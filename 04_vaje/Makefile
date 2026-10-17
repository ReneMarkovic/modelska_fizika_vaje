# ==============================================================================
# KONFIGURACIJA PREVAJALNIKA IN POTI
# ==============================================================================

# Prevajalnik in zastavice
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3 -g 
# -O3: Optimizacija za hitro delovanje (pomembno za simulacije)
# -g: Vključi simbole za razhroščevanje (debugging)
# -Wall, -Wextra: Vključi vsa opozorila

# Imena izhodnih datotek
TARGET = simulacija.exe

# Imena map
SRCDIR = src
BUILDDIR = obj
DATADIR = data

# Seznam vseh izvornih datotek (.cpp)
# Wildcard najde vse .cpp datoteke v mapi src/
SOURCES := $(wildcard $(SRCDIR)/*.cpp)

# Seznam objektnih datotek (.o), ki jih je treba ustvariti
# Zamenja src/X.cpp z obj/X.o
OBJECTS := $(patsubst $(SRCDIR)/%.cpp,$(BUILDDIR)/%.o,$(SOURCES))

# Zastavice za vključitev map (Headers)
INCLUDE_DIRS = -I$(SRCDIR)

# ==============================================================================
# NASTAVITVE ZA VIZUALIZACIJO/KNJIŽNICE (Priprava za npr. Raylib/OpenGL)
# ==============================================================================

# Če dodate Raylib, prilagodite naslednje vrstice:
# LDFLAGS = -L./lib/raylib -lraylib -lopengl32 -lgdi32 -lwinmm -lws2_32

# Zaenkrat uporabljamo samo sistemske knjižnice
LDFLAGS = -lm # -lm je pogosto potreben za matematiko na nekaterih sistemih

# ==============================================================================
# GLAVNA PRAVILA (Pravilo 'all' je privzeto)
# ==============================================================================

.PHONY: all clean run data

all: $(TARGET)

# Pravilo za ustvarjanje končne izvedljive datoteke
$(TARGET): $(OBJECTS)
	@echo "🔗 Povezovanje..."
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $@
	@echo "✅ Prevajanje končano: $@"

# Pravilo za ustvarjanje map (če ne obstajajo)
data:
	@mkdir -p $(DATADIR)
obj:
	@mkdir -p $(BUILDDIR)

# Pravilo za prevajanje posameznih .cpp datotek v objektne (.o) datoteke
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp | obj
	@echo "🔨 Prevajanje: $<"
	$(CXX) $(CXXFLAGS) $(INCLUDE_DIRS) -c $< -o $@

# ==============================================================================
# POMOŽNA PRAVILA
# ==============================================================================

# Zagon simulacije
run: $(TARGET) data
	@echo "▶️ Zagon simulacije..."
	./$(TARGET)

# Čiščenje projekta (izbriše .o datoteke in izvedljivo datoteko)
clean:
	@echo "🗑️ Čiščenje..."
	@rm -f $(OBJECTS) $(TARGET)
	@echo "🗑️ Odstranjene objektne datoteke in $(TARGET)."