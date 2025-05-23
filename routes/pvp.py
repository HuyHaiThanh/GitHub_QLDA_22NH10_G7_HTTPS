from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, make_response, flash
from models import User, Game, Move, Leaderboard, Skin, UserSkin, ReplayRequest
from extensions import db, socketio
from flask_socketio import emit, join_room, leave_room
import json
from datetime import datetime
import random
import string

pvp_bp = Blueprint('pvp', __name__)

@pvp_bp.route('/pvp/wait/<room_code>')
def wait_for_opponent(room_code):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name', next=request.url))
    
    game = Game.query.filter_by(room_code=room_code, status='waiting').first()
    if not game:
        return redirect(url_for('pvp_noti.index', error='Game room not found or already started.'))

    if str(game.player1_id) != user_id:
        return redirect(url_for('pvp_noti.index', error='Invalid access to waiting room.'))

    user = User.query.get(user_id)
    current_user_display_name = user.displayName if user else "Player 1"

    return render_template('wait_for_opponent.htm', room_code=room_code, game_id=game.game_id, display_name=current_user_display_name)

@pvp_bp.route('/pvp/game/<room_code>')
def pvp_game(room_code):
    user_id = request.cookies.get('user_id')
    game_id_cookie = request.cookies.get('game_id')

    if not user_id:
        return redirect(url_for('home.enter_name', next=request.url))

    game = None
    if game_id_cookie:
        game = Game.query.get(game_id_cookie)
        if game and game.room_code != room_code:
            # Game ID in cookie exists but is for a different room. Invalid state.
            # Log this or handle as an error. For now, treat as game not found by cookie.
            game = None
        elif game and game.status == 'finished': # Game from cookie is already finished
            game = None


    if not game:
        # Try to find an ongoing game in this room first
        game = Game.query.filter_by(room_code=room_code, status='ongoing').first()
        if not game:
            # If no ongoing game, try to find a waiting game (for P2 to join scenario)
            game = Game.query.filter_by(room_code=room_code, status='waiting').first()

    if not game:
        flash('Phòng game không tồn tại hoặc đã kết thúc.', 'error')
        return redirect(url_for('home.index'))

    # If a game was found by room_code (not by cookie) and a game_id_cookie exists,
    # they should ideally match if the user is supposed to be in this game.
    # This check is more of a sanity check.
    if game_id_cookie and str(game.game_id) != game_id_cookie and game.status == 'ongoing':
         # User has a cookie for a specific game, but the ongoing game found by room_code is different.
         # This could happen if they were redirected to a room with an old game_id cookie.
         # Prioritize the game found by room_code if it's ongoing.
         # Or, decide if this is an error state. For now, proceed with 'game' found by room_code.
         pass


    user = User.query.get(user_id)
    if not user:
        flash('Không tìm thấy thông tin người dùng.', 'error')
        return redirect(url_for('home.index', next=request.url))

    is_player1 = str(game.player1_id) == user_id
    is_player2 = game.player2_id and str(game.player2_id) == user_id

    if not is_player1 and not is_player2:
        # User is not in the game, attempt to join as Player 2 if game is waiting
        if game.status == 'waiting' and not game.player2_id:
            if str(game.player1_id) == user_id:
                 return redirect(url_for('pvp.wait_for_opponent', room_code=room_code))
            
            game.player2_id = user_id
            game.status = 'ongoing'
            db.session.commit()
            is_player2 = True # User successfully joined as P2
             # Emit event to notify P1 that P2 has joined
            socketio.emit('opponent_joined_direct', {
                'message': f'{user.displayName} has joined. The game will start!',
                'room_code': game.room_code,
                'player1_id': game.player1_id,
                'player1_name': User.query.get(game.player1_id).displayName,
                'player2_id': game.player2_id,
                'player2_name': user.displayName,
                'current_player_id': game.current_player_id,
                'game_id': game.game_id,
                'game_url': url_for('pvp.pvp_game', room_code=game.room_code, _external=True)
            }, room=game.room_code) # Emit to the room
        else:
            flash('Game này không còn chờ người chơi hoặc đã đầy.', 'error')
            return redirect(url_for('home.index'))
    
    if is_player1 and game.status == 'waiting' and not game.player2_id:
        return redirect(url_for('pvp.wait_for_opponent', room_code=room_code))

    if not (is_player1 or is_player2) and game.status == 'ongoing': # Check status ongoing here
         flash('Bạn không có quyền tham gia vào ván đấu này.', 'error')
         return redirect(url_for('home.index'))
    
    # If game status is finished, redirect to after_game page
    if game.status == 'finished':
        # Ensure the user is part of this finished game before redirecting
        if is_player1 or is_player2:
            return redirect(url_for('after_game.index', game_id=game.game_id))
        else:
            # User is not part of this finished game
            flash('Ván đấu này đã kết thúc và bạn không phải là người chơi.', 'error')
            return redirect(url_for('home.index'))


    opponent_id = game.player2_id if is_player1 else game.player1_id
    opponent = User.query.get(opponent_id) if opponent_id else None
    
    moves = Move.query.filter_by(game_id=game.game_id).order_by(Move.move_order).all()
    
    player1_obj_for_template = User.query.get(game.player1_id)
    player2_obj_for_template = User.query.get(game.player2_id) if game.player2_id else None
    
    # Lấy danh sách skin người dùng sở hữu
    user_skins = []
    if user: # Check if user object exists
        user_skins = db.session.query(Skin).join(UserSkin, UserSkin.skin_id == Skin.skin_id).filter(UserSkin.user_id == user.user_id).all()

    response = make_response(render_template('pvp.htm', 
                                            user=user,
                                            player1=player1_obj_for_template,
                                            player2=player2_obj_for_template,
                                            opponent=opponent,
                                            game=game, 
                                            moves=moves,
                                            is_player1=is_player1,
                                            room_code=game.room_code,
                                            user_skins=user_skins))
    response.set_cookie('game_id', str(game.game_id), max_age=60*60*24)
    return response

@socketio.on('join_pvp_room') # Renamed event
def on_join_pvp_room(data):
    room_param = data['room'] 
    user_id = request.cookies.get('user_id')
    game_id_cookie = request.cookies.get('game_id')

    if not user_id:
        emit('error', {'msg': 'User not identified.'}, room=request.sid)
        return

    user = User.query.get(user_id)
    if not user:
        emit('error', {'msg': 'User not found in database.'}, room=request.sid)
        return
        
    display_name = user.displayName

    game = None
    # Try to get game by cookie first, if it matches the room and is ongoing/waiting
    if game_id_cookie:
        temp_game = Game.query.get(game_id_cookie)
        if temp_game and temp_game.room_code == room_param and temp_game.status in ['ongoing', 'waiting']:
            # Check if current user is part of this game from cookie
            if str(temp_game.player1_id) == user_id or (temp_game.player2_id and str(temp_game.player2_id) == user_id):
                game = temp_game
    
    if not game:
        # If game not found by cookie or cookie was invalid for this room/user, find by room_code
        # Prioritize ongoing game for the room, then waiting game
        game = Game.query.filter_by(room_code=room_param, status='ongoing').first()
        if not game:
            game = Game.query.filter_by(room_code=room_param, status='waiting').first()

    if not game:
        emit('error', {'msg': f'Game room {room_param} not found or not in a joinable state.'}, room=request.sid)
        emit('force_redirect_home', {'reason': f'Phòng game {room_param} không tồn tại hoặc không thể tham gia.'}, room=request.sid)
        return

    # Ensure client joins the correct room name used for general game events
    join_room(game.room_code)
    print(f"{display_name} has joined room {game.room_code} (game_id: {game.game_id})")
    # Emit status to the specific room the user just joined
    emit('status', {'msg': f'{display_name} has joined the room.'}, room=game.room_code)
    
    # This event is primarily to notify player 1 when player 2 joins.
    # Player 2 joining via URL is now handled in pvp_game with 'opponent_joined_direct'.
    # This handler can still be useful if P2 joins via entering room code in pvp_noti.htm
    # or if P1 re-enters wait_for_opponent.htm.
    if game.player1_id and game.player2_id and game.status == 'ongoing':
        # This condition means both players are set and game is ongoing.
        # This is the point where P1 (if waiting) should be notified that P2 is in.
        player1 = User.query.get(game.player1_id)
        player2 = User.query.get(game.player2_id)
        
        # Check if the user emitting 'join_pvp_room' is actually P2
        # and P1 is the one to be notified.
        if str(game.player2_id) == user_id:
            print(f"[SocketIO on_join_pvp_room] P2 ({display_name}) confirmed in ongoing game. Notifying P1.")
            emit('opponent_joined', {
                'message': f'{player2.displayName} has joined. The game will start!',
                'room_code': game.room_code,
                'player1_id': game.player1_id, 
                'player1_name': player1.displayName,
                'player2_id': game.player2_id, 
                'player2_name': player2.displayName,
                'current_player_id': game.current_player_id,
                'game_id': game.game_id,
                'game_url': url_for('pvp.pvp_game', room_code=game.room_code, _external=True)
            }, room=game.room_code) # Emit to the room, P1 should get this in wait_for_opponent.htm
    elif game.status == 'waiting' and str(game.player1_id) == user_id:
        print(f"[SocketIO on_join_pvp_room] P1 ({display_name}) re-joined waiting room.")
        # P1 is in wait_for_opponent.htm, no need to emit 'opponent_joined' yet.

@socketio.on('leave_pvp_room') # Renamed event
def on_leave_pvp_room(data):
    room = data['room']
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    display_name = user.displayName if user else 'Anonymous'
    leave_room(room)
    print(f"{display_name} has left room {room}")
    emit('status', {'msg': f'{display_name} has left the room.'}, room=room)

@socketio.on('make_move')
def handle_move(data):
    print(f"[SocketIO] Received 'make_move' event with data: {data}")
    game_id = data.get('game_id')
    x = data.get('x')
    y = data.get('y')
    player_id = data.get('player_id')
    room = data.get('room')

    if not all([game_id, x is not None, y is not None, player_id, room]):
        print(f"[SocketIO] Invalid data received for 'make_move': {data}")
        emit('error', {'msg': 'Invalid move data received.'}, room=request.sid)
        return
    
    game = Game.query.get(game_id)
    if not game or game.status != 'ongoing':
        emit('error', {'msg': 'Game not found or not ongoing'}, room=room)
        return

    # Kiểm tra xem có đúng lượt của người chơi này không
    if str(game.current_player_id) != str(player_id):
        emit('error', {'msg': 'Not your turn!'}, room=request.sid) # Gửi lỗi về cho client vừa đi sai lượt
        print(f"[SocketIO] Invalid turn: User {player_id} tried to move, but current turn is for {game.current_player_id}")
        return
    
    existing_move = Move.query.filter_by(game_id=game_id, position_x=x, position_y=y).first()
    if existing_move:
        emit('error', {'msg': 'Position already taken'}, room=room)
        return
    
    last_move = Move.query.filter_by(game_id=game_id).order_by(Move.move_order.desc()).first()
    move_order = 1 if not last_move else last_move.move_order + 1
    
    # Create new move with combined position string
    new_move = Move(
        game_id=game_id,
        player_id=player_id,
        position=f"{x},{y}",  # Create combined position string
        move_order=move_order,
        position_x=x,
        position_y=y
    )
    
    db.session.add(new_move)
    db.session.commit()
    
    # Determine opponent_id for the next turn
    opponent_id = None
    if str(game.player1_id) == str(player_id):
        opponent_id = game.player2_id
    else:
        opponent_id = game.player1_id

    # Check for win
    if check_win(game_id, x, y, player_id):
        game.status = 'finished'
        game.winner_id = player_id
        # game.current_player_id = None # Optional: Clear current player on game end
        db.session.commit()
        
        update_leaderboard(player_id, True)
        if opponent_id: # Ensure opponent_id was found before updating their leaderboard
            update_leaderboard(opponent_id, False)
        
        emit('game_over', {
            'winner_id': player_id,
            'move': {
                'x': x,
                'y': y,
                'player_id': player_id
            }
        }, room=room)
    else:
        # Update current_player_id in the game
        game.current_player_id = opponent_id
        db.session.commit()

        emit('move_made', {
            'x': x,
            'y': y,
            'player_id': player_id,
            'next_player_id': opponent_id 
        }, room=room)

@socketio.on('time_up_forfeit')
def handle_time_up(data):
    game_id = data['game_id']
    player_id_timed_out = data['player_id']
    room = data['room']

    game = Game.query.get(game_id)
    if not game or game.status != 'ongoing':
        emit('error', {'msg': 'Game not found or already ended for time up forfeit.'}, room=room)
        return

    # Determine winner
    winner_id = None
    if str(game.player1_id) == str(player_id_timed_out):
        winner_id = game.player2_id
    elif str(game.player2_id) == str(player_id_timed_out):
        winner_id = game.player1_id
    else:
        # This shouldn't happen if player_id_timed_out is valid
        emit('error', {'msg': 'Invalid player ID for time out.'}, room=room)
        return

    game.status = 'finished'
    game.winner_id = winner_id
    db.session.commit()

    update_leaderboard(winner_id, True)
    update_leaderboard(player_id_timed_out, False)

    emit('game_over', {
        'winner_id': winner_id,
        'reason': f'Player {User.query.get(player_id_timed_out).displayName} ran out of time.'
    }, room=room)

@socketio.on('chat_message')
def handle_chat(data):
    room = data['room']
    message = data.get('message', '') # Use .get() for optional fields
    icon_url = data.get('icon_url') # Use .get() for optional fields
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id) 
    sender_name = user.displayName if user else session.get('display_name', 'Anonymous')
    
    emit('new_message', {
        'sender': sender_name,
        'message': message,
        'icon_url': icon_url, # Add icon_url to the emitted message
        'time': datetime.now().strftime('%H:%M')
    }, room=room)

@socketio.on('player_gave_up')
def handle_player_give_up(data):
    user_id = request.cookies.get('user_id')
    game_id = data.get('game_id')
    room_code = data.get('room')

    if not all([user_id, game_id, room_code]):
        emit('error', {'msg': 'Invalid give up request.'}, room=request.sid)
        print(f"Invalid give_up: user_id={user_id}, game_id={game_id}, room={room_code}")
        return

    game = Game.query.get(game_id)
    if not game:
        emit('error', {'msg': 'Game not found for give up.'}, room=request.sid)
        print(f"Give_up error: Game {game_id} not found.")
        return

    if game.room_code != room_code:
        emit('error', {'msg': 'Room mismatch for give up.'}, room=request.sid)
        print(f"Give_up error: Game {game_id} room_code {game.room_code} != received room {room_code}.")
        return

    if game.status != 'ongoing':
        emit('error', {'msg': 'Game not ongoing, cannot give up.'}, room=request.sid)
        print(f"Give_up error: Game {game_id} status is {game.status}.")
        return

    giving_up_player = User.query.get(user_id)
    if not giving_up_player:
        emit('error', {'msg': 'User not found for give up.'}, room=request.sid)
        print(f"Give_up error: User {user_id} not found.")
        return

    winner_id = None
    if str(game.player1_id) == user_id:
        winner_id = game.player2_id
    elif str(game.player2_id) == user_id:
        winner_id = game.player1_id
    else:
        emit('error', {'msg': 'You are not a player in this game to give up.'}, room=request.sid)
        print(f"Give_up error: User {user_id} is not a player in game {game_id}.")
        return
    
    if not winner_id: # Should not happen if the above logic is correct and game has two players
        emit('error', {'msg': 'Could not determine winner after give up.'}, room=room_code)
        print(f"Give_up error: Could not determine winner for game {game_id} after user {user_id} gave up.")
        return

    game.status = 'finished'
    game.winner_id = winner_id
    db.session.commit()

    update_leaderboard(winner_id, True)
    update_leaderboard(user_id, False) # User who gave up loses

    reason_message = f'{giving_up_player.displayName} đã từ bỏ.'
    print(f"Game {game_id} ended. Winner: {winner_id}. Reason: {reason_message}")

    socketio.emit('game_over', {
        'winner_id': winner_id,
        'reason': reason_message,
        'gave_up_player_id': user_id
    }, room=room_code)

    # Tell the giving up player's client to redirect
    emit('redirect_after_action', {
        'message': 'Bạn đã từ bỏ ván đấu.',
        'category': 'info',
        'redirect_url': url_for('home.index')
    }, room=request.sid) # request.sid is the specific client who emitted 'player_gave_up'

# Helper functions
def check_win(game_id, x, y, player_id):
    # Get all moves for this game
    moves = Move.query.filter_by(game_id=game_id, player_id=player_id).all()
    
    # Create a board representation
    board = [[0 for _ in range(15)] for _ in range(15)]
    for move in moves:
        board[move.position_y][move.position_x] = 1
    
    # Check for 5 in a row
    directions = [
        [(0, 1), (0, -1)],   # Vertical
        [(1, 0), (-1, 0)],   # Horizontal
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]   # Diagonal \
    ]
    
    for dir_pair in directions:
        count = 1  # Count the piece we just placed
        
        # Check in both directions
        for dx, dy in dir_pair:
            nx, ny = x, y
            
            # Count consecutive pieces in this direction
            for _ in range(4):  # Need 4 more to make 5 in a row
                nx, ny = nx + dx, ny + dy
                if (0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == 1):
                    count += 1
                else:
                    break
            
        if count >= 5:
            return True
    
    return False

def update_leaderboard(user_id, is_win):
    leaderboard = Leaderboard.query.filter_by(user_id=user_id).first()
    if not leaderboard:
        leaderboard = Leaderboard(user_id=user_id,
                                wins=0, 
                                losses=0, 
                                total_games=0, 
                                win_rate=0.0)
        db.session.add(leaderboard)
    else:
        # Đảm bảo các giá trị không phải là None nếu bản ghi đã tồn tại nhưng có thể có giá trị null từ DB (ít khả năng nếu default hoạt động)
        if leaderboard.wins is None: leaderboard.wins = 0
        if leaderboard.losses is None: leaderboard.losses = 0
        if leaderboard.total_games is None: leaderboard.total_games = 0
        if leaderboard.win_rate is None: leaderboard.win_rate = 0.0
    
    leaderboard.total_games += 1
    if is_win:
        leaderboard.wins += 1
    else:
        leaderboard.losses += 1
    
    if leaderboard.total_games > 0:
        leaderboard.win_rate = round((leaderboard.wins / leaderboard.total_games) * 100, 2) # Tính tỷ lệ phần trăm, làm tròn 2 chữ số
    else:
        leaderboard.win_rate = 0.0
    
    db.session.commit()

# Helper function to create a new PvP rematch
def create_new_pvp_rematch(original_game_id, player1_id, player2_id):
    new_room_code = ''.join(random.choices(string.digits, k=6))
    
    # Determine who goes first in the new game (e.g., alternate or P1 of old game is P1 of new)
    # For simplicity, let's say player1_id argument is the one to start
    # You might want to fetch the original game to decide who was P1/P2 if roles need to be swapped or preserved.
    original_game = Game.query.get(original_game_id)
    new_current_player_id = player1_id # Defaulting to player1_id passed to function
    if original_game:
        # Example: Alternate first player - if original game's P1 was player1_id, new P1 is player2_id
        if str(original_game.player1_id) == str(player1_id) and str(original_game.current_player_id) == str(player1_id): # If P1 started last game
             #This logic might be more complex if you track first player explicitly.
             #For now, let's simplify: if P1 starts, P2 starts next, or keep it random or fixed.
             #Let's make P2 (the other player) start if P1 (current requester's role in old game) started last.
             #This requires knowing original P1.
             #Simplest: player1_id (who is P1 for new game) starts.
             pass # player1_id (as P1 for new game) starts

    new_game = Game(
        player1_id=player1_id,
        player2_id=player2_id,
        status='ongoing',
        room_code=new_room_code,
        current_player_id=new_current_player_id 
    )
    db.session.add(new_game)
    
    ReplayRequest.query.filter_by(game_id=original_game_id).delete()
    db.session.commit()
    return new_game

@socketio.on('replay_request')
def handle_replay_request(data):
    room = data.get('room') # room_code of the old game
    game_id = data.get('game_id')
    user_id = request.cookies.get('user_id')
    
    if not all([user_id, room, game_id]):
        emit('error', {'msg': 'Invalid replay request. Missing data.'}, room=request.sid)
        # No direct redirect from here as it's a socket event, client should handle UI
        print(f"Invalid replay request: user_id={user_id}, room={room}, game_id={game_id}")
        return

    game = Game.query.get(game_id)
    # Verify room_code matches game_id's game for consistency
    if not game or game.room_code != room:
        emit('error', {'msg': 'Game not found or room mismatch for replay.'}, room=request.sid)
        emit('force_redirect_home', {'reason': 'Thông tin phòng game cho việc chơi lại không hợp lệ.'}, room=request.sid)
        print(f"Replay error: Game {game_id} not found or room {room} mismatch.")
        return

    if game.status != 'finished':
        emit('error', {'msg': 'Game not in a replayable state (not finished).'}, room=request.sid)
        # No direct redirect as client is already on pvp page, but good to inform if an error occurs.
        print(f"Replay error: Game {game_id} status is {game.status}, not 'finished'.")
        return

    # Record replay request
    existing_request = ReplayRequest.query.filter_by(game_id=game.game_id, player_id=user_id).first()
    if not existing_request:
        replay_req = ReplayRequest(game_id=game.game_id, player_id=user_id)
        db.session.add(replay_req)
        db.session.commit()
        print(f"User {user_id} requested replay for game {game.game_id} in room {room}")

    # Determine opponent
    opponent_id = None
    if str(game.player1_id) == user_id:
        opponent_id = game.player2_id
    elif str(game.player2_id) == user_id:
        opponent_id = game.player1_id
    
    if not opponent_id:
        print(f"Replay error: Could not determine opponent for user {user_id} in game {game.game_id}.")
        return 

    opponent_request = ReplayRequest.query.filter_by(game_id=game.game_id, player_id=opponent_id).first()

    if opponent_request:
        print(f"Both players ({user_id}, {opponent_id}) ready for rematch from game {game.game_id}")
        
        # Determine P1 and P2 for the new game.
        # For simplicity, original P1 remains P1, original P2 remains P2.
        # You can implement logic to swap roles or decide randomly.
        p1_new_game = game.player1_id
        p2_new_game = game.player2_id
        
        new_game = create_new_pvp_rematch(game.game_id, p1_new_game, p2_new_game)
        
        print(f"New game created: ID {new_game.game_id}, Room {new_game.room_code}. Emitting to old room {game.room_code}")
        socketio.emit('start_new_pvp_game', 
                      {'new_room_code': new_game.room_code, 'new_game_id': new_game.game_id}, 
                      room=game.room_code) # Emit to the old game's room
    else:
        # Notify opponent that this player wants a rematch
        requesting_user = User.query.get(user_id)
        if requesting_user:
            socketio.emit('opponent_wants_replay', 
                          {'player_name': requesting_user.displayName}, 
                          room=game.room_code) # Emit to the old game's room
            print(f"User {user_id} ({requesting_user.displayName}) wants replay. Notified opponent {opponent_id} in room {game.room_code}")