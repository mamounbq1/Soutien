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

    # --- Teacher Operations ---
    def add_teacher(self, nom, prenom, matiere, tel, salaire_horaire):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO teachers (nom, prenom, matiere, tel, salaire_horaire)
            VALUES (?, ?, ?, ?, ?)
        ''', (nom, prenom, matiere, tel, salaire_horaire))
        conn.commit()
        conn.close()

    def get_all_teachers(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM teachers ORDER BY id DESC')
        data = cursor.fetchall()
        conn.close()
        return data

    def search_teachers(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM teachers 
            WHERE nom LIKE ? OR prenom LIKE ? OR matiere LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_teacher(self, teacher_id, nom, prenom, matiere, tel, salaire_horaire):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE teachers 
            SET nom=?, prenom=?, matiere=?, tel=?, salaire_horaire=?
            WHERE id=?
        ''', (nom, prenom, matiere, tel, salaire_horaire, teacher_id))
        conn.commit()
        conn.close()

    def delete_teacher(self, teacher_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM teachers WHERE id=?', (teacher_id,))
        conn.commit()
        conn.close()

    # --- Subject Operations ---
    def add_subject(self, nom, description, tarif_mensuel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO subjects (nom, description, tarif_mensuel)
            VALUES (?, ?, ?)
        ''', (nom, description, tarif_mensuel))
        conn.commit()
        conn.close()

    def get_all_subjects(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subjects ORDER BY id DESC')
        data = cursor.fetchall()
        conn.close()
        return data

    def search_subjects(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM subjects 
            WHERE nom LIKE ? OR description LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_subject(self, subject_id, nom, description, tarif_mensuel):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE subjects 
            SET nom=?, description=?, tarif_mensuel=?
            WHERE id=?
        ''', (nom, description, tarif_mensuel, subject_id))
        conn.commit()
        conn.close()

    def delete_subject(self, subject_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM subjects WHERE id=?', (subject_id,))
        conn.commit()
        conn.close()

    # --- Group Operations ---
    def add_group(self, nom, matiere_id, prof_id, salle):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO groups (nom, matiere_id, prof_id, salle)
            VALUES (?, ?, ?, ?)
        ''', (nom, matiere_id, prof_id, salle))
        conn.commit()
        conn.close()

    def get_all_groups(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT g.id, g.nom, s.nom as matiere, t.nom || ' ' || t.prenom as prof, g.salle
            FROM groups g
            LEFT JOIN subjects s ON g.matiere_id = s.id
            LEFT JOIN teachers t ON g.prof_id = t.id
            ORDER BY g.id DESC
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_group_details(self, group_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM groups WHERE id=?', (group_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def search_groups(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT g.id, g.nom, s.nom as matiere, t.nom || ' ' || t.prenom as prof, g.salle
            FROM groups g
            LEFT JOIN subjects s ON g.matiere_id = s.id
            LEFT JOIN teachers t ON g.prof_id = t.id
            WHERE g.nom LIKE ? OR s.nom LIKE ? OR g.salle LIKE ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_group(self, group_id, nom, matiere_id, prof_id, salle):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE groups 
            SET nom=?, matiere_id=?, prof_id=?, salle=?
            WHERE id=?
        ''', (nom, matiere_id, prof_id, salle, group_id))
        conn.commit()
        conn.close()

    def delete_group(self, group_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM groups WHERE id=?', (group_id,))
        conn.commit()
        conn.close()

    # --- Inscription Operations ---
    def add_inscription(self, student_id, group_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inscriptions (student_id, group_id)
            VALUES (?, ?)
        ''', (student_id, group_id))
        conn.commit()
        conn.close()

    def get_group_students(self, group_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.nom, s.prenom, s.tel, i.date_inscription
            FROM students s
            JOIN inscriptions i ON s.id = i.student_id
            WHERE i.group_id = ?
            ORDER BY s.nom
        ''', (group_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    # --- Payment Operations ---
    def add_payment(self, student_id, montant, mois, annee):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO paiements (student_id, montant, mois, annee)
            VALUES (?, ?, ?, ?)
        ''', (student_id, montant, mois, annee))
        conn.commit()
        conn.close()

    def get_all_payments(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, s.nom || ' ' || s.prenom as student, p.montant, p.mois, p.annee, p.date_paiement
            FROM paiements p
            JOIN students s ON p.student_id = s.id
            ORDER BY p.date_paiement DESC
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

    def get_student_payments(self, student_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, montant, mois, annee, date_paiement
            FROM paiements
            WHERE student_id = ?
            ORDER BY date_paiement DESC
        ''', (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    def search_payments(self, query):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, s.nom || ' ' || s.prenom as student, p.montant, p.mois, p.annee, p.date_paiement
            FROM paiements p
            JOIN students s ON p.student_id = s.id
            WHERE s.nom LIKE ? OR s.prenom LIKE ? OR p.mois LIKE ?
            ORDER BY p.date_paiement DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        data = cursor.fetchall()
        conn.close()
        return data

    def delete_payment(self, payment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM paiements WHERE id=?', (payment_id,))
        conn.commit()
        conn.close()

    def get_monthly_revenue(self, mois, annee):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COALESCE(SUM(montant), 0)
            FROM paiements
            WHERE mois = ? AND annee = ?
        ''', (mois, annee))
        revenue = cursor.fetchone()[0]
        conn.close()
        return revenue

    # --- Presence Operations ---
    def add_presence(self, group_id, student_id, date_seance, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO presence (group_id, student_id, date_seance, status)
            VALUES (?, ?, ?, ?)
        ''', (group_id, student_id, date_seance, status))
        conn.commit()
        conn.close()

    def get_presence_by_group_date(self, group_id, date_seance):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, s.id, s.nom, s.prenom, p.status
            FROM presence p
            JOIN students s ON p.student_id = s.id
            WHERE p.group_id = ? AND p.date_seance = ?
        ''', (group_id, date_seance))
        data = cursor.fetchall()
        conn.close()
        return data

    def update_presence(self, presence_id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE presence 
            SET status = ?
            WHERE id = ?
        ''', (status, presence_id))
        conn.commit()
        conn.close()

    def check_presence_exists(self, group_id, student_id, date_seance):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM presence
            WHERE group_id = ? AND student_id = ? AND date_seance = ?
        ''', (group_id, student_id, date_seance))
        result = cursor.fetchone()
        conn.close()
        return result

# Quick test
if __name__ == "__main__":
    db = DatabaseManager()
