import {createBoard, playMove} from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
    // Init the UI
    const board = document.querySelector(".board");
    createBoard(board);
});