#include <ncurses.h>
#include <string>
#include <vector>

class TextEditor {
public:
    TextEditor() {
        initscr();
        noecho();
        keypad(stdscr, TRUE);
        getmaxyx(stdscr, max_y, max_x);
        buffer.push_back("");  // Start with an empty line
        cursor_x = 0;
        cursor_y = 0;
        wrap_width = 40;  // Set fixed wrap width
        view_start = 0;   // Track the starting line of the view
    }

    ~TextEditor() {
        endwin();
    }

    void run() {
        while (true) {
            render();
            int ch = getch();
            handle_input(ch);
            if (ch == 'q') {  // Quit on 'q'
                break;
            }
        }
    }

private:
    std::vector<std::string> buffer;
    int cursor_x, cursor_y;
    int max_x, max_y;
    int wrap_width;
    int view_start; // The starting line of the viewable window

    void render() {
        clear();
        int lines_to_display = max_y;
        for (int i = 0; i < lines_to_display && view_start + i < buffer.size(); ++i) {
            mvprintw(i, 0, buffer[view_start + i].c_str());
        }
        move(cursor_y - view_start, cursor_x); // Adjust for view_start
        refresh();
    }

    void handle_input(int ch) {
        switch (ch) {
            case KEY_F1:
                exit();
                break;
            case KEY_UP:
                if (cursor_y > 0) {
                    cursor_y--;
                }
                if (cursor_y < view_start) {
                    view_start--;
                }
                if (cursor_x > buffer[cursor_y].length()) {
                    cursor_x = buffer[cursor_y].length();
                }
                break;
            case KEY_DOWN:
                if (cursor_y < buffer.size() - 1) {
                    cursor_y++;
                }
                if (cursor_y >= view_start + max_y) {
                    view_start++;
                }
                if (cursor_x > buffer[cursor_y].length()) {
                    cursor_x = buffer[cursor_y].length();
                }
                break;
            case KEY_LEFT:
                if (cursor_x > 0) {
                    cursor_x--;
                }
                break;
            case KEY_RIGHT:
                if (cursor_x < buffer[cursor_y].length()) {
                    cursor_x++;
                }
                break;
            case KEY_BACKSPACE:
            case 127:  // Handle backspace
                if (cursor_x > 0) {
                    buffer[cursor_y].erase(cursor_x - 1, 1);
                    cursor_x--;
                } else if (cursor_y > 0) {
                    cursor_x = buffer[cursor_y - 1].length();
                    buffer[cursor_y - 1] += buffer[cursor_y];
                    buffer.erase(buffer.begin() + cursor_y);
                    cursor_y--;
                    if (cursor_y < view_start) {
                        view_start--;
                    }
                }
                break;
            case KEY_ENTER:
            case 10:  // Enter key
                buffer.insert(buffer.begin() + cursor_y + 1, buffer[cursor_y].substr(cursor_x));
                buffer[cursor_y] = buffer[cursor_y].substr(0, cursor_x);
                cursor_y++;
                cursor_x = 0;
                if (cursor_y >= view_start + max_y) {
                    view_start++;
                }
                break;
            default:
                if (isprint(ch)) {
                    buffer[cursor_y].insert(cursor_x, 1, ch);
                    cursor_x++;
                }
                break;
        }
        word_wrap();
    }

    void word_wrap() {
        for (size_t i = 0; i < buffer.size(); ++i) {
            while (buffer[i].length() > wrap_width) {
                size_t wrap_pos = buffer[i].rfind(' ', wrap_width);
                if (wrap_pos == std::string::npos) {
                    wrap_pos = wrap_width;
                } else {
                    wrap_pos += 1; // Include the space character in the move
                }

                std::string overflow = buffer[i].substr(wrap_pos);
                buffer[i] = buffer[i].substr(0, wrap_pos);
                buffer.insert(buffer.begin() + i + 1, overflow);

                if (cursor_y == i && cursor_x >= wrap_pos) {
                    cursor_y++;
                    if (cursor_y >= view_start + max_y) {
                        view_start++;
                    }
                    cursor_x -= wrap_pos;
                } else if (cursor_y > i) {
                    cursor_y++;
                    if (cursor_y >= view_start + max_y) {
                        view_start++;
                    }
                }
            }
        }
    }
};

int main() {
    TextEditor editor;
    editor.run();
    return 0;
}
