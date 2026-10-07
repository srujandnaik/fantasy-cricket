import sys
import sqlite3

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QListWidget,
    QInputDialog,
    QLabel,
    QPushButton,
    QRadioButton,
    QLineEdit,
)
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


DATABASE_NAME = "fantasy_cricket.db"
TOTAL_POINTS = 1000
MAX_PLAYERS = 11


class FantasyCricket:

    def __init__(self):

        # =====================================================
        # LOAD UI
        # =====================================================

        ui_file = QFile("fantasy_cricket.ui")

        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(
                "Could not open fantasy_cricket.ui"
            )

        loader = QUiLoader()

        self.window = loader.load(ui_file)

        ui_file.close()

        if self.window is None:
            raise RuntimeError(
                "Could not load fantasy_cricket.ui"
            )

        # Show menu inside the window on macOS
        self.window.menuBar().setNativeMenuBar(False)

        # =====================================================
        # TEAM VARIABLES
        # =====================================================

        self.team_name = ""
        self.selected_players = []
        self.points_used = 0

        # =====================================================
        # LIST WIDGETS
        # =====================================================

        self.list_available = self.window.findChild(
            QListWidget,
            "listAvailablePlayers"
        )

        self.list_selected = self.window.findChild(
            QListWidget,
            "listSelectedPlayers"
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.btn_add = self.window.findChild(
            QPushButton,
            "btnAddPlayer"
        )

        self.btn_remove = self.window.findChild(
            QPushButton,
            "btnRemovePlayer"
        )

        self.btn_clear = self.window.findChild(
            QPushButton,
            "btnClearTeam"
        )

        self.btn_evaluate = self.window.findChild(
            QPushButton,
            "btnEvaluateTeam"
        )

        self.btn_save = self.window.findChild(
            QPushButton,
            "btnSaveTeam"
        )

        # =====================================================
        # RADIO BUTTONS
        # =====================================================

        self.radio_bat = self.window.findChild(
            QRadioButton,
            "radioBAT"
        )

        self.radio_bowl = self.window.findChild(
            QRadioButton,
            "radioBOWL"
        )

        self.radio_ar = self.window.findChild(
            QRadioButton,
            "radioAR"
        )

        self.radio_wk = self.window.findChild(
            QRadioButton,
            "radioWK"
        )

        # Make category buttons mutually exclusive
        self.radio_bat.setAutoExclusive(True)
        self.radio_bowl.setAutoExclusive(True)
        self.radio_ar.setAutoExclusive(True)
        self.radio_wk.setAutoExclusive(True)

        # =====================================================
        # LABELS
        # =====================================================

        self.label_selected = self.window.findChild(
            QLabel,
            "labelSelectedPlayers"
        )

        self.label_points_available = self.window.findChild(
            QLabel,
            "labelPointsAvailable"
        )

        self.label_points_used = self.window.findChild(
            QLabel,
            "labellabelPointsUsed"
        )

        # Give Points Used enough space so "120" is not clipped
        self.label_points_used.setMinimumWidth(180)

        self.label_batsmen = self.window.findChild(
            QLabel,
            "labelBatsmen"
        )

        self.label_bowlers = self.window.findChild(
            QLabel,
            "labelBowlers"
        )

        self.label_all_rounders = self.window.findChild(
            QLabel,
            "labelAllRounders"
        )

        self.label_wicket_keeper = self.window.findChild(
            QLabel,
            "labelWicketKeeper"
        )

        # =====================================================
        # TEAM NAME
        # =====================================================

        self.team_name_field = self.window.findChild(
            QLineEdit,
            "lineTeamName"
        )

        # =====================================================
        # MENU ACTIONS
        # =====================================================

        self.action_new = self.window.findChild(
            QAction,
            "actionNew_Team"
        )

        self.action_open = self.window.findChild(
            QAction,
            "actionOpen_team"
        )

        self.action_save = self.window.findChild(
            QAction,
            "actionSave_Team"
        )

        self.action_evaluate = self.window.findChild(
            QAction,
            "actionEvaluate_Team"
        )

        # =====================================================
        # BUTTON CONNECTIONS
        # =====================================================

        self.btn_add.clicked.connect(
            self.add_player
        )

        self.btn_remove.clicked.connect(
            self.remove_player
        )

        self.btn_clear.clicked.connect(
            self.clear_team
        )

        self.btn_save.clicked.connect(
            self.save_team
        )

        self.btn_evaluate.clicked.connect(
            self.evaluate_team
        )

        # =====================================================
        # DOUBLE-CLICK CONNECTIONS
        # =====================================================

        self.list_available.itemDoubleClicked.connect(
            self.add_player
        )

        self.list_selected.itemDoubleClicked.connect(
            self.remove_player
        )

        # =====================================================
        # RADIO BUTTON CONNECTIONS
        # =====================================================

        self.radio_bat.clicked.connect(
            self.load_players
        )

        self.radio_bowl.clicked.connect(
            self.load_players
        )

        self.radio_ar.clicked.connect(
            self.load_players
        )

        self.radio_wk.clicked.connect(
            self.load_players
        )

        # =====================================================
        # MENU CONNECTIONS
        # =====================================================

        self.action_new.triggered.connect(
            self.new_team
        )

        self.action_open.triggered.connect(
            self.open_team
        )

        self.action_save.triggered.connect(
            self.save_team
        )

        self.action_evaluate.triggered.connect(
            self.evaluate_team
        )

        # =====================================================
        # INITIAL STATE
        # =====================================================

        self.disable_selection()

        self.radio_bat.setChecked(True)

        self.update_points_display()

        self.update_category_counts()

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def get_connection(self):

        try:

            return sqlite3.connect(
                DATABASE_NAME
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not connect to database.\n\n{error}"
            )

            return None

    # =========================================================
    # ENABLE SELECTION
    # =========================================================

    def enable_selection(self):

        self.list_available.setEnabled(True)
        self.list_selected.setEnabled(True)

        self.btn_add.setEnabled(True)
        self.btn_remove.setEnabled(True)
        self.btn_clear.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.btn_evaluate.setEnabled(True)

        self.radio_bat.setEnabled(True)
        self.radio_bowl.setEnabled(True)
        self.radio_ar.setEnabled(True)
        self.radio_wk.setEnabled(True)

    # =========================================================
    # DISABLE SELECTION
    # =========================================================

    def disable_selection(self):

        self.list_available.setEnabled(False)
        self.list_selected.setEnabled(False)

        self.btn_add.setEnabled(False)
        self.btn_remove.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_evaluate.setEnabled(False)

        self.radio_bat.setEnabled(False)
        self.radio_bowl.setEnabled(False)
        self.radio_ar.setEnabled(False)
        self.radio_wk.setEnabled(False)

    # =========================================================
    # NEW TEAM
    # =========================================================

    def new_team(self):

        team_name, ok = QInputDialog.getText(
            self.window,
            "New Team",
            "Enter team name:"
        )

        if not ok:
            return

        team_name = team_name.strip()

        if not team_name:

            QMessageBox.warning(
                self.window,
                "Invalid Team Name",
                "Please enter a team name."
            )

            return

        self.team_name = team_name

        self.selected_players = []

        self.points_used = 0

        self.team_name_field.setText(
            team_name
        )

        self.list_selected.clear()

        self.enable_selection()

        self.radio_bat.setChecked(True)

        self.load_players()

        self.update_points_display()

        self.update_category_counts()

        self.show_status(
            f"New team '{team_name}' created."
        )

    # =========================================================
    # GET SELECTED CATEGORY
    # =========================================================

    def get_selected_category(self):

        if self.radio_bat.isChecked():
            return "BAT"

        if self.radio_bowl.isChecked():
            return "BWL"

        if self.radio_ar.isChecked():
            return "AR"

        if self.radio_wk.isChecked():
            return "WK"

        return "BAT"

    # =========================================================
    # LOAD PLAYERS
    # =========================================================

    def load_players(self):

        if not self.team_name:
            return

        category = self.get_selected_category()

        connection = self.get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT player, value
                FROM stats
                WHERE ctg = ?
                ORDER BY player
                """,
                (category,)
            )

            players = cursor.fetchall()

            self.list_available.clear()

            for player, value in players:

                if player not in self.selected_players:

                    self.list_available.addItem(
                        f"{player} ({value} points)"
                    )

            self.show_status(
                f"{len(players)} players loaded."
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not load players.\n\n{error}"
            )

        finally:

            connection.close()

    # =========================================================
    # GET PLAYER VALUE
    # =========================================================

    def get_player_value(self, player):

        connection = self.get_connection()

        if connection is None:
            return None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT value
                FROM stats
                WHERE player = ?
                """,
                (player,)
            )

            result = cursor.fetchone()

            if result:

                return result[0]

            return None

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not get player value.\n\n{error}"
            )

            return None

        finally:

            connection.close()

    # =========================================================
    # GET PLAYER CATEGORY
    # =========================================================

    def get_player_category(self, player):

        connection = self.get_connection()

        if connection is None:
            return None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT ctg
                FROM stats
                WHERE player = ?
                """,
                (player,)
            )

            result = cursor.fetchone()

            if result:

                return result[0]

            return None

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not get player category.\n\n{error}"
            )

            return None

        finally:

            connection.close()

    # =========================================================
    # ADD PLAYER
    # =========================================================

    def add_player(self, item=None):

        if not self.team_name:

            QMessageBox.warning(
                self.window,
                "Create Team",
                "Please create a new team first."
            )

            return

        if item is None:

            item = self.list_available.currentItem()

        if item is None:

            QMessageBox.information(
                self.window,
                "Select Player",
                "Please select a player."
            )

            return

        player = item.text().split(" (")[0].strip()

        # Maximum 11 players
        if len(self.selected_players) >= MAX_PLAYERS:

            QMessageBox.warning(
                self.window,
                "Selection Limit",
                "You can select a maximum of 11 players."
            )

            return

        value = self.get_player_value(player)

        if value is None:
            return

        # Points validation
        if self.points_used + value > TOTAL_POINTS:

            QMessageBox.warning(
                self.window,
                "Points Limit",
                "You do not have enough points available "
                "to select this player."
            )

            return

        category = self.get_player_category(player)

        # Only one wicket keeper
        if category == "WK":

            if self.count_category("WK") >= 1:

                QMessageBox.warning(
                    self.window,
                    "Selection Rule",
                    "Only one wicket-keeper can be selected."
                )

                return

        # Add player
        self.selected_players.append(player)

        self.points_used += value

        self.refresh_selected_list()

        self.load_players()

        self.update_points_display()

        self.update_category_counts()

    # =========================================================
    # REMOVE PLAYER
    # =========================================================

    def remove_player(self, item=None):

        if item is None:

            item = self.list_selected.currentItem()

        if item is None:

            QMessageBox.information(
                self.window,
                "Select Player",
                "Please select a player to remove."
            )

            return

        player = item.text().strip()

        value = self.get_player_value(player)

        if value is None:
            return

        if player in self.selected_players:

            self.selected_players.remove(player)

            self.points_used -= value

        if self.points_used < 0:

            self.points_used = 0

        self.refresh_selected_list()

        self.load_players()

        self.update_points_display()

        self.update_category_counts()

    # =========================================================
    # REFRESH SELECTED LIST
    # =========================================================

    def refresh_selected_list(self):

        self.list_selected.clear()

        for player in self.selected_players:

            self.list_selected.addItem(
                player
            )

    # =========================================================
    # COUNT CATEGORY
    # =========================================================

    def count_category(self, category):

        count = 0

        for player in self.selected_players:

            if self.get_player_category(player) == category:

                count += 1

        return count

    # =========================================================
    # UPDATE CATEGORY COUNTS
    # =========================================================

    def update_category_counts(self):

        batsmen = self.count_category("BAT")

        bowlers = self.count_category("BWL")

        all_rounders = self.count_category("AR")

        wicketkeepers = self.count_category("WK")

        self.label_batsmen.setText(
            f"Batsmen ({batsmen})"
        )

        self.label_bowlers.setText(
            f"Bowlers ({bowlers})"
        )

        self.label_all_rounders.setText(
            f"All-rounders ({all_rounders})"
        )

        self.label_wicket_keeper.setText(
            f"Wicket-keeper ({wicketkeepers})"
        )

        self.label_selected.setText(
            f"Selected Players ({len(self.selected_players)})"
        )

    # =========================================================
    # UPDATE POINTS
    # =========================================================

    def update_points_display(self):

        available = TOTAL_POINTS - self.points_used

        self.label_points_available.setText(
            f"Points Available: {available}"
        )

        self.label_points_used.setText(
            f"Points Used: {self.points_used}"
        )

    # =========================================================
    # CLEAR TEAM
    # =========================================================

    def clear_team(self):

        if not self.selected_players:
            return

        answer = QMessageBox.question(
            self.window,
            "Clear Team",
            "Are you sure you want to clear the team?"
        )

        if answer != QMessageBox.Yes:
            return

        self.selected_players = []

        self.points_used = 0

        self.list_selected.clear()

        self.load_players()

        self.update_points_display()

        self.update_category_counts()

        self.show_status(
            "Team cleared."
        )

    # =========================================================
    # VALIDATE TEAM
    # =========================================================

    def validate_team(self):

        if not self.team_name:

            QMessageBox.warning(
                self.window,
                "Team Name Required",
                "Please create a team first."
            )

            return False

        if len(self.selected_players) != 11:

            QMessageBox.warning(
                self.window,
                "Invalid Team",
                "You must select exactly 11 players.\n\n"
                f"Currently selected: "
                f"{len(self.selected_players)}"
            )

            return False

        if self.count_category("WK") != 1:

            QMessageBox.warning(
                self.window,
                "Invalid Team",
                "Please select exactly one wicket-keeper."
            )

            return False

        return True

    # =========================================================
    # SAVE TEAM
    # =========================================================

    def save_team(self):

        if not self.validate_team():
            return

        connection = self.get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            players = ", ".join(
                self.selected_players
            )

            cursor.execute(
                """
                INSERT OR REPLACE INTO teams
                (name, players, value)
                VALUES (?, ?, ?)
                """,
                (
                    self.team_name,
                    players,
                    self.points_used
                )
            )

            connection.commit()

            QMessageBox.information(
                self.window,
                "Team Saved",
                f"Team '{self.team_name}' saved successfully."
            )

            self.show_status(
                f"Team '{self.team_name}' saved."
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not save team.\n\n{error}"
            )

        finally:

            connection.close()

    # =========================================================
    # OPEN TEAM
    # =========================================================

    def open_team(self):

        connection = self.get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name, players, value
                FROM teams
                ORDER BY name
                """
            )

            teams = cursor.fetchall()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not open teams.\n\n{error}"
            )

            return

        finally:

            connection.close()

        if not teams:

            QMessageBox.information(
                self.window,
                "No Teams",
                "No saved teams found."
            )

            return

        team_names = [
            team[0]
            for team in teams
        ]

        team_name, ok = QInputDialog.getItem(
            self.window,
            "Open Team",
            "Select team:",
            team_names,
            0,
            False
        )

        if not ok:
            return

        selected_team = None

        for team in teams:

            if team[0] == team_name:

                selected_team = team

                break

        if selected_team is None:
            return

        self.team_name = selected_team[0]

        self.team_name_field.setText(
            self.team_name
        )

        self.selected_players = [
            player.strip()
            for player in selected_team[1].split(",")
            if player.strip()
        ]

        self.points_used = 0

        for player in self.selected_players:

            value = self.get_player_value(player)

            if value is not None:

                self.points_used += value

        self.enable_selection()

        self.refresh_selected_list()

        self.load_players()

        self.update_points_display()

        self.update_category_counts()

        QMessageBox.information(
            self.window,
            "Team Opened",
            f"Team '{self.team_name}' opened successfully."
        )

    # =========================================================
    # CALCULATE PLAYER SCORE
    # =========================================================

    def calculate_player_score(self, player):

        connection = self.get_connection()

        if connection is None:
            return 0

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    scored,
                    faced,
                    fours,
                    sixes,
                    bowled,
                    maiden,
                    given,
                    wkts,
                    catches,
                    stumping,
                    ro
                FROM match
                WHERE player = ?
                """,
                (player,)
            )

            data = cursor.fetchone()

            if data is None:
                return 0

            (
                scored,
                faced,
                fours,
                sixes,
                bowled,
                maiden,
                given,
                wkts,
                catches,
                stumping,
                run_outs
            ) = data

            score = 0

            # -------------------------
            # BATTING
            # -------------------------

            # 1 point for every 2 runs
            score += scored // 2

            # Century / half-century bonus
            if scored >= 100:

                score += 10

            elif scored >= 50:

                score += 5

            # Strike rate bonus
            if faced > 0:

                strike_rate = (
                    scored / faced
                ) * 100

                if 80 <= strike_rate <= 100:

                    score += 2

                elif strike_rate > 100:

                    score += 4

            # Fours and sixes
            score += fours

            score += sixes * 2

            # -------------------------
            # BOWLING
            # -------------------------

            # 10 points per wicket
            score += wkts * 10

            # Wicket bonus
            if wkts >= 5:

                score += 10

            elif wkts >= 3:

                score += 5

            # Economy rate
            if bowled > 0:

                overs = bowled / 6

                economy = given / overs

                if economy < 2:

                    score += 10

                elif economy < 3.5:

                    score += 7

                elif economy <= 4.5:

                    score += 4

            # -------------------------
            # FIELDING
            # -------------------------

            score += catches * 10

            score += stumping * 10

            score += run_outs * 10

            return score

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not calculate score.\n\n{error}"
            )

            return 0

        finally:

            connection.close()

    # =========================================================
    # CALCULATE TEAM SCORE
    # =========================================================

    def calculate_team_score(self, players):

        total_score = 0

        for player in players:

            total_score += (
                self.calculate_player_score(player)
            )

        return total_score

    # =========================================================
    # EVALUATE TEAM
    # =========================================================

    def evaluate_team(self):

        connection = self.get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name, players
                FROM teams
                ORDER BY name
                """
            )

            teams = cursor.fetchall()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Could not retrieve teams.\n\n{error}"
            )

            return

        finally:

            connection.close()

        if not teams:

            QMessageBox.information(
                self.window,
                "No Saved Teams",
                "Please save a team before evaluating."
            )

            return

        team_names = [
            team[0]
            for team in teams
        ]

        team_name, ok = QInputDialog.getItem(
            self.window,
            "Evaluate Team",
            "Select your team:",
            team_names,
            0,
            False
        )

        if not ok:
            return

        selected_team = None

        for team in teams:

            if team[0] == team_name:

                selected_team = team

                break

        if selected_team is None:
            return

        players = [
            player.strip()
            for player in selected_team[1].split(",")
            if player.strip()
        ]

        total_score = self.calculate_team_score(
            players
        )

        QMessageBox.information(
            self.window,
            "Fantasy Team Score",
            f"Team: {team_name}\n\n"
            f"Players: {len(players)}\n"
            f"Fantasy Score: {total_score} points"
        )

        self.show_status(
            f"{team_name} scored {total_score} points."
        )

    # =========================================================
    # STATUS BAR
    # =========================================================

    def show_status(self, message):

        self.window.statusBar().showMessage(
            message
        )

    # =========================================================
    # SHOW WINDOW
    # =========================================================

    def show(self):

        self.window.show()


# =============================================================
# MAIN
# =============================================================

def main():

    app = QApplication(sys.argv)

    try:

        fantasy_cricket = FantasyCricket()

        fantasy_cricket.show()

        sys.exit(
            app.exec()
        )

    except Exception as error:

        QMessageBox.critical(
            None,
            "Application Error",
            f"The application could not start.\n\n{error}"
        )

        sys.exit(1)


if __name__ == "__main__":

    main()