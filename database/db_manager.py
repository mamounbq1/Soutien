import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="database/app.db"):
        self.db_name = db_name
        self.check_db_exists()

    def check_db_exists(self):
        if not os.path.exists(os.path.dirname(self.db_name)):
            os.makedirs(os.path.dirname(self.db_name))
        
        if not os.path.exists(self.db_name):
            self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # A. Table élèves
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            niveau TEXT,
            filiere TEXT,
            tel TEXT,
            parent_tel TEXT,
            date_inscription DATE DEFAULT (datetime('now','localtime'))
        )
        ''')

        # B. Table enseignants
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            matiere TEXT,
            tel TEXT,
            salaire_horaire REAL
        )
        ''')

        # C. Table matières
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            tarif_mensuel REAL
        )
        ''')

        # D. Table groupes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            matiere_id INTEGER,
            prof_id INTEGER,
            salle TEXT,
            FOREIGN KEY(matiere_id) REFERENCES subjects(id),
            FOREIGN KEY(prof_id) REFERENCES teachers(id)
        )
        ''')

        # E. Table inscriptions (Relation Student-Group)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            group_id INTEGER,
            date_inscription DATE DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(group_id) REFERENCES groups(id)
        )
        ''')

        # F. Table paiements
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            montant REAL,
            mois TEXT,
            annee TEXT,
            date_paiement DATE DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        ''')

        # G. Table présence
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS presence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            student_id INTEGER,
            date_seance DATE,
            status TEXT, -- 'present', 'absent', 'retard'
            FOREIGN KEY(group_id) REFERENCES groups(id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        ''')
        
        # H. Table Utilisateurs (Auth)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
        ''')
        
        # Insert default admin if not exists
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            # In production, password should be hashed!
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")

        conn.commit()
        conn.close()
        print("Database initialized successfully.")

    # --- Student Operations ---
    def add_student(self, nom, prenom, niveau, filiere, tel, parent_tel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (nom, prenom, niveau, filiere, tel, parent_tel)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nom, prenom, niveau, filiere, tel, parent_tel))
        conn.commit()
        conn.close()

    def get_all_students(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY id DESC')
        data = cursor.fetchall()
        conn.close()
        return data

    def search_students(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM students 
            WHERE nom LIKE ? OR prenom LIKE ? OR tel LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_student(self, student_id, nom, prenom, niveau, filiere, tel, parent_tel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students 
            SET nom=?, prenom=?, niveau=?, filiere=?, tel=?, parent_tel=?
            WHERE id=?
        ''', (nom, prenom, niveau, filiere, tel, parent_tel, student_id))
        conn.commit()
        conn.close()

    def delete_student(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id=?', (student_id,))
        conn.commit()
        conn.close()
    
    def get_student_inscriptions(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.date_inscription, g.nom, s.nom 
            FROM inscriptions i
            JOIN groups g ON i.group_id = g.id
            JOIN subjects s ON g.matiere_id = s.id
            WHERE i.student_id = ?
            ORDER BY i.date_inscription DESC
        ''', (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

# Quick test
if __name__ == "__main__":
    db = DatabaseManager()
