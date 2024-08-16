CXX = g++
CXXFLAGS = -lncurses
TARGET = notepad
SRC = notepad.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) -o $(TARGET) $(SRC) $(CXXFLAGS)

clean:
	rm -f $(TARGET)
