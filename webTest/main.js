import {createBoard, playMove} from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
    // Init the UI
    const board = document.querySelector(".board");
    createBoard(board);

    // Open the Websocket connection and register event handlers
    const websocket = new WebSocket("ws://localhost:8001/");
    sendMoves(board, websocket);
});

function sendMoves(board, websocket) {
    // When clicking a column, send a "play" event for a move in that column
    board.addEventListener("Click", ({ target }) => {
        const column = target.dataset.column;
        // Ignore clicks outside a column
        if (column === undefined) {
            return;
        }
        const event = {
            type: "play",
            column: parseInt(column, 10),
        };
        websocket.send(JSON.stringify(event));
    });
}