CXX = g++
CXXFLAGS = -lncurses
TARGET = gnotepad
SRC = gnotepad.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) -o $(TARGET) $(SRC) $(CXXFLAGS)

clean:
	rm -f $(TARGET)
