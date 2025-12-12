const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Serve static files from the current directory
app.use(express.static(__dirname));

// Serve the main file specifically at root if index.html doesn't exist or is different
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'golf_club.html'));
});

io.on('connection', (socket) => {
    console.log('A user connected');

    // Send a welcome message
    socket.emit('status_update', { message: 'Connected to Real-Time Server', status: 'connected' });

    // Simulate a random news update broadcast every 10 seconds to show it working
    const interval = setInterval(() => {
        const events = [
            "New Tournament Announced: Summer Splash!",
            "Course Maintenance: Hole 7 closed tomorrow.",
            "Pro Shop Sale: 20% off all irons.",
            "Weather Alert: Sunny skies expected all week.",
            "Member Spotlight: John Doe hits a Hole-in-One!"
        ];
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        const date = new Date().toLocaleDateString();

        io.emit('news_update', {
            title: "Live Update",
            date: date,
            description: randomEvent,
            force_reload: false
        });
    }, 10000);

    socket.on('disconnect', () => {
        console.log('User disconnected');
        clearInterval(interval);
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
    console.log('Open http://localhost:3000 in your browser');
});
