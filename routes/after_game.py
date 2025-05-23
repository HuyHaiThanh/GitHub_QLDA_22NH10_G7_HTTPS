from flask import Blueprint, render_template, redirect, url_for, request, make_response
from models import User, Game, Move, ReplayRequest
from app import db, socketio
from flask_socketio import emit, join_room
import random
import string

after_game_bp = Blueprint('after_game', __name__)

@socketio.on('join_after_game_notifications')
def on_join_after_game_notifications(data):
    room_code = data.get('room_code')
    user_id = request.cookies.get('user_id')
    if not room_code or not user_id:
        print(f"[SocketIO join_after_game_notifications] Missing room_code or user_id. Data: {data}, User: {user_id}")
        return
    
    user = User.query.get(user_id)
    if not user:
        print(f"[SocketIO join_after_game_notifications] User {user_id} not found.")
        return

    join_room(room_code)
    print(f"User {user.displayName} (ID: {user_id}) joined notification room: {room_code} from after_game/waiting_replay page.")

    game = Game.query.filter_by(room_code=room_code).first()
    if game:
        is_player_in_game = (game.player1_id and str(game.player1_id) == str(user_id)) or \
                            (game.player2_id and str(game.player2_id) == str(user_id))
        
        if game.status == 'ongoing' and is_player_in_game:
            print(f"Catch-up: Game {game.game_id} (room {room_code}) is 'ongoing'. Emitting game_restart to user {user_id} ({request.sid}).")
            emit('game_restart', {
                'new_game_id': game.game_id,
                'room_code': game.room_code,
                'current_player_id': game.current_player_id
            }, room=request.sid)

@after_game_bp.route('/after_game/<int:game_id>')
def index(game_id):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    game = Game.query.get(game_id)
    if not game:
        return redirect(url_for('home.index'))
    user = User.query.get(user_id)
    if not user:
        from routes.home import create_new_user
        display_name = request.cookies.get('display_name')
        user = create_new_user(user_id, display_name)
    winner = User.query.get(game.winner_id) if game.winner_id else None
    is_pve = game.player2_id is None
    opponent = None
    if not is_pve and game.player1_id and game.player2_id:
        current_user_is_player1 = str(game.player1_id) == str(user_id)
        opponent_id = game.player2_id if current_user_is_player1 else game.player1_id
        if opponent_id:
            opponent = User.query.get(opponent_id)
    moves_count = Move.query.filter_by(game_id=game_id).count()
    return render_template('after_game.htm', 
                          user=user, 
                          game=game, 
                          winner=winner,
                          is_pve=is_pve,
                          opponent=opponent,
                          moves_count=moves_count)

@after_game_bp.route('/replay/<int:game_id>')
def replay(game_id):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    original_game = Game.query.get(game_id)
    if not original_game:
        return redirect(url_for('home.index'))
    user = User.query.get(user_id)
    if not user:
        from routes.home import create_new_user
        display_name = request.cookies.get('display_name')
        user = create_new_user(user_id, display_name)
    is_pve = original_game.player2_id is None
    if is_pve:
        new_pve_game = Game(
            player1_id=user_id,
            player2_id=None,
            status='ongoing',
            room_code=f"pve_{random.randint(100000, 999999)}"
        )
        db.session.add(new_pve_game)
        db.session.commit()
        response = make_response(redirect(url_for('pve.index')))
        response.set_cookie('game_id', str(new_pve_game.game_id), max_age=60*60*24)
        return response
    else:
        if not original_game.player1_id or not original_game.player2_id:
            return redirect(url_for('home.index'))
        existing_request = ReplayRequest.query.filter_by(
            game_id=original_game.game_id,
            player_id=user_id
        ).first()
        if not existing_request:
            replay_request = ReplayRequest(
                game_id=original_game.game_id,
                player_id=user_id
            )
            db.session.add(replay_request)
            db.session.commit()
        socketio.emit('replay_ready', {
            'player_id': user_id,
            'game_id': original_game.game_id,
            'user_display_name': user.displayName
        }, room=original_game.room_code)
        opponent_id = original_game.player2_id if str(original_game.player1_id) == str(user_id) else original_game.player1_id
        opponent_request = ReplayRequest.query.filter_by(
            game_id=original_game.game_id,
            player_id=opponent_id
        ).first()
        if opponent_request:
            Move.query.filter_by(game_id=original_game.game_id).delete()
            original_game.status = 'ongoing'
            original_game.winner_id = None
            original_game.current_player_id = random.choice([original_game.player1_id, original_game.player2_id])
            ReplayRequest.query.filter_by(game_id=original_game.game_id).delete()
            db.session.commit()
            print(f"Game {original_game.game_id} (Room: {original_game.room_code}) reset for replay. Current player: {original_game.current_player_id}")
            socketio.emit('game_restart', {
                'new_game_id': original_game.game_id,
                'room_code': original_game.room_code,
                'current_player_id': original_game.current_player_id
            }, room=original_game.room_code)
            response = make_response(redirect(url_for('pvp.pvp_game', room_code=original_game.room_code)))
            response.set_cookie('game_id', str(original_game.game_id), max_age=60*60*24)
            return response
        return render_template('waiting_replay.htm', game=original_game, user=user)

@after_game_bp.route('/leave_room/<int:game_id>')
def leave_room(game_id):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('home.enter_name'))
    game = Game.query.get(game_id)
    if not game:
        return redirect(url_for('home.index'))
    ReplayRequest.query.filter_by(game_id=game_id).delete()
    db.session.commit()
    if game.player2_id:
        socketio.emit('player_left', {
            'player_id': user_id,
            'message': f"Đối thủ đã rời khỏi phòng chờ chơi lại."
        }, room=game.room_code)
    response = make_response(redirect(url_for('home.index')))
    response.delete_cookie('game_id')
    return response