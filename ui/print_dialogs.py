"""
Dialogues d'impression pour les PDF
Gère l'interface utilisateur pour imprimer :
- Emplois du temps par groupe
- Factures élèves
- Fiches de paie professeurs
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme
from widgets.modern_components import *
from utils.pdf_generator import PDFGenerator


class PrintScheduleDialog(ctk.CTkToplevel):
    """Dialogue pour imprimer l'emploi du temps d'un groupe"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.pdf_generator = PDFGenerator()
        
        self.title("🖨️ Imprimer Emploi du Temps")
        self.geometry("500x350")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._load_groups()
        self._create_ui()
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _load_groups(self):
        """Charger tous les groupes"""
        groups_data = self.db_manager.get_all_groups()
        self.groups_dict = {f"{g[1]} (ID: {g[0]})": g for g in groups_data}
    
    def _create_ui(self):
        """Créer l'interface"""
        # Titre
        title = ModernLabel(
            self,
            text="📅 Imprimer Emploi du Temps",
            style='heading',
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(30, 10))
        
        subtitle = ModernLabel(
            self,
            text="Sélectionnez un groupe pour générer son emploi du temps",
            style='secondary'
        )
        subtitle.pack(pady=(0, 30))
        
        # Carte de formulaire
        form_card = ModernCard(self)
        form_card.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Sélection du groupe
        ModernLabel(form_card, text="Groupe *", style='label').pack(anchor="w", padx=20, pady=(20, 5))
        
        self.group_combo = ModernComboBox(
            form_card,
            values=list(self.groups_dict.keys()) if self.groups_dict else ["Aucun groupe"],
            width=400
        )
        self.group_combo.pack(padx=20, pady=(0, 20))
        
        if self.groups_dict:
            self.group_combo.set(list(self.groups_dict.keys())[0])
        
        # Boutons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ModernButton(
            btn_frame,
            text="Annuler",
            command=self.destroy,
            style='secondary',
            width=180
        ).pack(side="left", padx=(0, 10))
        
        ModernButton(
            btn_frame,
            text="🖨️ Générer PDF",
            command=self._generate_pdf,
            style='primary',
            width=180
        ).pack(side="left")
    
    def _generate_pdf(self):
        """Générer le PDF de l'emploi du temps"""
        if not self.groups_dict:
            messagebox.showerror("Erreur", "Aucun groupe disponible.")
            return
        
        selected_group_key = self.group_combo.get()
        if not selected_group_key or selected_group_key == "Aucun groupe":
            messagebox.showerror("Erreur", "Veuillez sélectionner un groupe.")
            return
        
        group_data_tuple = self.groups_dict[selected_group_key]
        group_id = group_data_tuple[0]
        
        # Préparer les données du groupe
        group_data = {
            'id': group_data_tuple[0],
            'nom': group_data_tuple[1],
            'matiere': group_data_tuple[2] if len(group_data_tuple) > 2 else 'N/A',
            'niveau': group_data_tuple[3] if len(group_data_tuple) > 3 else 'N/A'
        }
        
        # Récupérer les séances du groupe
        sessions_raw = self.db_manager.get_schedule_by_group(group_id)
        sessions_data = []
        for session in sessions_raw:
            sessions_data.append({
                'jour': session[1],
                'periode': session[2],
                'heure_debut': session[3],
                'heure_fin': session[4],
                'prof': session[5],
                'salle': session[6]
            })
        
        # Récupérer les étudiants du groupe
        students_raw = self.db_manager.get_group_students(group_id)
        students_list = []
        for student in students_raw:
            students_list.append({
                'nom': student[1],
                'prenom': student[2],
                'tel': student[3] if len(student) > 3 else 'N/A'
            })
        
        # Générer le PDF
        try:
            pdf_path = self.pdf_generator.generate_group_schedule(
                group_data,
                sessions_data,
                students_list
            )
            
            messagebox.showinfo(
                "✅ Succès",
                f"PDF généré avec succès !\n\nEmplacement : {pdf_path}"
            )
            
            # Demander si ouvrir le fichier
            if messagebox.askyesno("Ouvrir le fichier", "Voulez-vous ouvrir le PDF ?"):
                os.startfile(pdf_path) if os.name == 'nt' else os.system(f'xdg-open "{pdf_path}"')
            
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")


class PrintStudentInvoiceDialog(ctk.CTkToplevel):
    """Dialogue pour imprimer une facture élève"""
    
    def __init__(self, parent, db_manager, student_id=None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.pdf_generator = PDFGenerator()
        self.student_id = student_id
        
        self.title("🖨️ Imprimer Facture Élève")
        self.geometry("550x600")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._load_data()
        self._create_ui()
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _load_data(self):
        """Charger les étudiants"""
        students_data = self.db_manager.get_all_students()
        self.students_dict = {f"{s[1]} {s[2]} (ID: {s[0]})": s for s in students_data}
    
    def _create_ui(self):
        """Créer l'interface"""
        # Titre
        title = ModernLabel(
            self,
            text="💰 Imprimer Facture Élève",
            style='heading',
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(30, 10))
        
        subtitle = ModernLabel(
            self,
            text="Générez un reçu de paiement pour un élève",
            style='secondary'
        )
        subtitle.pack(pady=(0, 30))
        
        # Carte de formulaire
        form_card = ModernCard(self)
        form_card.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Sélection de l'élève
        ModernLabel(form_card, text="Élève *", style='label').pack(anchor="w", padx=20, pady=(20, 5))
        
        self.student_combo = ModernComboBox(
            form_card,
            values=list(self.students_dict.keys()) if self.students_dict else ["Aucun élève"],
            width=450
        )
        self.student_combo.pack(padx=20, pady=(0, 15))
        
        if self.students_dict:
            self.student_combo.set(list(self.students_dict.keys())[0])
        
        # Montant
        ModernLabel(form_card, text="Montant (DH) *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.amount_entry = ModernEntry(form_card, placeholder="Ex: 500", width=450)
        self.amount_entry.pack(padx=20, pady=(0, 15))
        
        # Mois
        ModernLabel(form_card, text="Mois *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.month_combo = ModernComboBox(
            form_card,
            values=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
            width=450
        )
        self.month_combo.pack(padx=20, pady=(0, 15))
        self.month_combo.set("Janvier")
        
        # Année
        ModernLabel(form_card, text="Année *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.year_entry = ModernEntry(form_card, placeholder="Ex: 2024", width=450)
        self.year_entry.pack(padx=20, pady=(0, 20))
        self.year_entry.insert(0, "2024")
        
        # Boutons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ModernButton(
            btn_frame,
            text="Annuler",
            command=self.destroy,
            style='secondary',
            width=200
        ).pack(side="left", padx=(0, 10))
        
        ModernButton(
            btn_frame,
            text="🖨️ Générer Facture",
            command=self._generate_invoice,
            style='primary',
            width=200
        ).pack(side="left")
    
    def _generate_invoice(self):
        """Générer la facture PDF"""
        if not self.students_dict:
            messagebox.showerror("Erreur", "Aucun élève disponible.")
            return
        
        selected_student_key = self.student_combo.get()
        if not selected_student_key or selected_student_key == "Aucun élève":
            messagebox.showerror("Erreur", "Veuillez sélectionner un élève.")
            return
        
        # Validation montant
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Erreur", "Montant invalide.")
            return
        
        # Validation année
        try:
            year = int(self.year_entry.get())
            if year < 2000 or year > 2100:
                raise ValueError()
        except:
            messagebox.showerror("Erreur", "Année invalide.")
            return
        
        student_data_tuple = self.students_dict[selected_student_key]
        
        # Préparer les données de l'élève
        student_data = {
            'id': student_data_tuple[0],
            'nom': student_data_tuple[1],
            'prenom': student_data_tuple[2],
            'niveau': student_data_tuple[3] if len(student_data_tuple) > 3 else 'N/A',
            'tel': student_data_tuple[5] if len(student_data_tuple) > 5 else 'N/A'
        }
        
        # Préparer les données de paiement
        payment_data = {
            'montant': amount,
            'mois': self.month_combo.get(),
            'annee': year,
            'date_paiement': datetime.now().strftime('%d/%m/%Y'),
            'ref': f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        # Informations de l'école
        school_info = {
            'nom': 'Centre de Soutien Scolaire',
            'adresse': 'Adresse de l\'établissement',
            'tel': '0500000000',
            'email': 'contact@centre.ma'
        }
        
        # Générer le PDF
        try:
            pdf_path = self.pdf_generator.generate_student_invoice(
                student_data,
                payment_data,
                school_info
            )
            
            messagebox.showinfo(
                "✅ Succès",
                f"Facture générée avec succès !\n\nEmplacement : {pdf_path}"
            )
            
            # Demander si ouvrir le fichier
            if messagebox.askyesno("Ouvrir le fichier", "Voulez-vous ouvrir le PDF ?"):
                os.startfile(pdf_path) if os.name == 'nt' else os.system(f'xdg-open "{pdf_path}"')
            
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")


class PrintTeacherPayslipDialog(ctk.CTkToplevel):
    """Dialogue pour imprimer une fiche de paie professeur"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.pdf_generator = PDFGenerator()
        
        self.title("🖨️ Imprimer Fiche de Paie")
        self.geometry("550x550")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=(ModernTheme.BG_LIGHT, ModernTheme.BG_DARK))
        
        self._load_data()
        self._create_ui()
        self._center_window()
    
    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _load_data(self):
        """Charger les professeurs"""
        teachers_data = self.db_manager.get_all_teachers()
        self.teachers_dict = {f"{t[1]} {t[2]} (ID: {t[0]})": t for t in teachers_data}
    
    def _create_ui(self):
        """Créer l'interface"""
        # Titre
        title = ModernLabel(
            self,
            text="📄 Imprimer Fiche de Paie",
            style='heading',
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(30, 10))
        
        subtitle = ModernLabel(
            self,
            text="Générez une fiche de paie pour un professeur",
            style='secondary'
        )
        subtitle.pack(pady=(0, 30))
        
        # Carte de formulaire
        form_card = ModernCard(self)
        form_card.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Sélection du professeur
        ModernLabel(form_card, text="Professeur *", style='label').pack(anchor="w", padx=20, pady=(20, 5))
        
        self.teacher_combo = ModernComboBox(
            form_card,
            values=list(self.teachers_dict.keys()) if self.teachers_dict else ["Aucun professeur"],
            width=450
        )
        self.teacher_combo.pack(padx=20, pady=(0, 15))
        
        if self.teachers_dict:
            self.teacher_combo.set(list(self.teachers_dict.keys())[0])
        
        # Heures travaillées
        ModernLabel(form_card, text="Heures travaillées *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.hours_entry = ModernEntry(form_card, placeholder="Ex: 40", width=450)
        self.hours_entry.pack(padx=20, pady=(0, 15))
        
        # Mois
        ModernLabel(form_card, text="Mois *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.month_combo = ModernComboBox(
            form_card,
            values=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
            width=450
        )
        self.month_combo.pack(padx=20, pady=(0, 15))
        self.month_combo.set("Janvier")
        
        # Année
        ModernLabel(form_card, text="Année *", style='label').pack(anchor="w", padx=20, pady=(10, 5))
        self.year_entry = ModernEntry(form_card, placeholder="Ex: 2024", width=450)
        self.year_entry.pack(padx=20, pady=(0, 20))
        self.year_entry.insert(0, "2024")
        
        # Boutons
        btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ModernButton(
            btn_frame,
            text="Annuler",
            command=self.destroy,
            style='secondary',
            width=200
        ).pack(side="left", padx=(0, 10))
        
        ModernButton(
            btn_frame,
            text="🖨️ Générer Fiche",
            command=self._generate_payslip,
            style='primary',
            width=200
        ).pack(side="left")
    
    def _generate_payslip(self):
        """Générer la fiche de paie PDF"""
        if not self.teachers_dict:
            messagebox.showerror("Erreur", "Aucun professeur disponible.")
            return
        
        selected_teacher_key = self.teacher_combo.get()
        if not selected_teacher_key or selected_teacher_key == "Aucun professeur":
            messagebox.showerror("Erreur", "Veuillez sélectionner un professeur.")
            return
        
        # Validation heures
        try:
            hours = float(self.hours_entry.get())
            if hours <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Erreur", "Nombre d'heures invalide.")
            return
        
        # Validation année
        try:
            year = int(self.year_entry.get())
            if year < 2000 or year > 2100:
                raise ValueError()
        except:
            messagebox.showerror("Erreur", "Année invalide.")
            return
        
        teacher_data_tuple = self.teachers_dict[selected_teacher_key]
        
        # Préparer les données du professeur
        teacher_data = {
            'id': teacher_data_tuple[0],
            'nom': teacher_data_tuple[1],
            'prenom': teacher_data_tuple[2],
            'matiere': teacher_data_tuple[3] if len(teacher_data_tuple) > 3 else 'N/A',
            'tel': teacher_data_tuple[4] if len(teacher_data_tuple) > 4 else 'N/A',
            'salaire_horaire': teacher_data_tuple[5] if len(teacher_data_tuple) > 5 else 0
        }
        
        # Préparer les données de travail
        work_data = {
            'mois': self.month_combo.get(),
            'annee': year,
            'heures_travaillees': hours,
            'sessions_list': []  # Peut être étendu pour récupérer les séances réelles
        }
        
        # Informations de l'école
        school_info = {
            'nom': 'Centre de Soutien Scolaire',
            'adresse': 'Adresse de l\'établissement',
            'tel': '0500000000'
        }
        
        # Générer le PDF
        try:
            pdf_path = self.pdf_generator.generate_teacher_payslip(
                teacher_data,
                work_data,
                school_info
            )
            
            messagebox.showinfo(
                "✅ Succès",
                f"Fiche de paie générée avec succès !\n\nEmplacement : {pdf_path}"
            )
            
            # Demander si ouvrir le fichier
            if messagebox.askyesno("Ouvrir le fichier", "Voulez-vous ouvrir le PDF ?"):
                os.startfile(pdf_path) if os.name == 'nt' else os.system(f'xdg-open "{pdf_path}"')
            
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")


# Import manquant
from datetime import datetime
