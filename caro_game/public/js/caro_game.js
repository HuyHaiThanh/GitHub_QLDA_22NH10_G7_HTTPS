// JavaScript cho ứng dụng Caro Game
frappe.provide("caro_game");

// Khởi tạo ứng dụng Caro Game
caro_game = {
    init: function() {
        // Khởi tạo các module
        this.initModules();
        
        // Thiết lập các event listeners
        this.setupEventListeners();
        
        console.log("Caro Game initialized");
    },
    
    initModules: function() {
        // Khởi tạo các module của ứng dụng
        this.game = caro_game.game;
        this.authentication = caro_game.authentication;
        this.analytics = caro_game.analytics;
        this.player = caro_game.player;
        this.game_core = caro_game.game_core;
    },
    
    setupEventListeners: function() {
        // Thiết lập các event listeners
        $(document).on("app_ready", function() {
            console.log("Caro Game app ready");
        });
    }
};

// Module Game
caro_game.game = {
    init: function() {
        console.log("Game module initialized");
    },
    
    createGame: function(options) {
        return frappe.call({
            method: "caro_game.game.doctype.game.game.create_game",
            args: options
        });
    },
    
    makeMove: function(gameId, x, y, skillId) {
        return frappe.call({
            method: "caro_game.game.doctype.move.move.make_move",
            args: {
                game_id: gameId,
                position_x: x,
                position_y: y,
                skill_id: skillId || null
            }
        });
    }
};

// Module Authentication
caro_game.authentication = {
    init: function() {
        console.log("Authentication module initialized");
    },
    
    register: function(userData) {
        return frappe.call({
            method: "caro_game.authentication.api.register",
            args: userData
        });
    },
    
    login: function(username, password) {
        return frappe.call({
            method: "caro_game.authentication.api.login",
            args: {
                username: username,
                password: password
            }
        });
    }
};

// Khởi tạo khi document ready
$(document).ready(function() {
    caro_game.init();
});