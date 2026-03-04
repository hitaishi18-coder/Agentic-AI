# Todo App (Generated via CLI Agent)

This directory contains a simple, functional To-Do List web application. 

**Note on Origin:** This entire application—including the HTML structure, CSS styling, and JavaScript logic—was autonomously generated and saved to the filesystem by the AI agent built in the `05 cli agent` directory. It serves as a practical demonstration of an agent's ability to execute system commands and write code.

## Overview

The application is a classic frontend project built with standard web technologies. It allows users to type a task into an input field and add it to a growing list below.

## Files

* **`index.html`**: The main structure of the application. It contains the input field, the "Add" button, an empty unordered list (`<ul>`) for the tasks, and links to the CSS and JS files.
* **`style.css`**: Provides a clean, centered, and modern UI. It styles the input box, adds hover effects to the green "Add" button, and styles the list items with bottom borders.
* **`app.js`**: Contains the core logic. The `addTodo()` function reads the text from the input, creates a new list item (`<li>`), appends it to the list, and then clears the input field for the next task.

## Usage

Because this is a vanilla frontend application without any server-side dependencies, running it is incredibly simple:

1. Simply double-click the `index.html` file in your file explorer to open it in your default web browser.
2. Type a task into the input box and click **Add**.