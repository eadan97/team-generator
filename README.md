# ⚽ Team Generator

A web app for creating balanced and customizable soccer teams, designed for quick match setup and fair play. Easily manage players, input stats, and generate multiple team variations with constraints.


## TODO list

- ~~Migrar los pesos a nuevo formato~~
- ~~cargar los nuevos pesos~~
- ~~mostrar los pesos actuales~~
- actualizar los pesos
- mostrar ponderado de los pesos
- actualizar modelo de OR para el nuevo formato
- Borrar todo lo que no se usa. 

---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/eadan97/team-generator.git
    cd team-generator
    ```

2. **Create and activate a Conda environment (recommended):**
    ```bash
    conda env create -f environment.yml
    conda activate team-generator
    ```

3. **Run the app:**
    ```bash
    streamlit run app.py
    ```

---

## ✨ Features

- Player management: Add, edit, and remove players with individual stats.
- Team generation: Create balanced teams based on player stats and constraints.
- Multiple variations: Generate several team combinations for each match.
- Restriction support: Prevent specific player pairs from being on the same team.
- Interactive UI: Easy-to-use Streamlit interface for quick setup and results.

---

## 🖥️ Usage

1. Launch the app and navigate to the Player Manager to manage your player list and stats.
2. Go to the Team Generator page to select players, set team size, and generate teams.
3. Review team variations and stats summaries to choose the best matchup.

*Screenshots and detailed examples coming soon!*

---

## ⚙️ Configuration

- Edit `config.yml` to customize player stats, team size limits, and other options.
- Player data is stored in `data/players.json` for persistence. * We might migrate this in the near future.*

---

## 🤝 Contributing

Contributions are welcome!  
To contribute:
- Fork the repo and create a new branch for your feature or bugfix.
- Submit a pull request with a clear description.
- For issues or feature requests, please open an issue on GitHub.

Also, you could contact me and be added to the contributor list.

---

## 📄 License

[MIT License](LICENSE) &mdash; see the LICENSE file for details.

---

## 📊 Player Stats

- **Pace**
- **Shooting**
- **Passing**
- **Dribbling**
- **Defending**
- **Physical**

---

## 👥 People

Adan, Artavia, Birrita, Bryan, Chaco, Charlie, Dan, Emma, Kevin, Mauro, Santi, Andrey, Rolo, Teclas

---