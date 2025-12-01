"""
Module de génération de PDF pour le système de gestion
Gère 3 types de documents :
1. Emploi du temps par groupe
2. Facture de paiement élève
3. Fiche de paie professeur
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class PDFGenerator:
    """Classe principale pour générer les PDF"""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def _get_styles(self):
        """Styles de base pour les documents"""
        styles = getSampleStyleSheet()
        
        # Style titre principal
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E40AF'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Style sous-titre
        styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Style normal
        styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
        
        return styles
    
    # ========================
    # 1. EMPLOI DU TEMPS GROUPE
    # ========================
    
    def generate_group_schedule(self, group_data, sessions_data, students_list):
        """
        Génère un emploi du temps pour un groupe avec liste des étudiants
        
        Args:
            group_data: dict avec {id, nom, matiere, niveau}
            sessions_data: list de dict avec {jour, periode, heure_debut, heure_fin, prof, salle}
            students_list: list de dict avec {nom, prenom, tel}
        
        Returns:
            str: Chemin du fichier PDF généré
        """
        filename = f"emploi_temps_{group_data['nom']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Créer le document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=40
        )
        
        # Construire le contenu
        story = []
        styles = self._get_styles()
        
        # En-tête
        story.append(Paragraph("📅 EMPLOI DU TEMPS", styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informations du groupe
        group_info = f"""
        <b>Groupe:</b> {group_data['nom']}<br/>
        <b>Matière:</b> {group_data.get('matiere', 'N/A')}<br/>
        <b>Niveau:</b> {group_data.get('niveau', 'N/A')}<br/>
        <b>Date d'édition:</b> {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        """
        story.append(Paragraph(group_info, styles['CustomNormal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Tableau de l'emploi du temps
        if sessions_data:
            story.append(Paragraph("📋 Séances programmées", styles['CustomSubtitle']))
            
            # Données du tableau
            table_data = [
                ['Jour', 'Période', 'Horaire', 'Professeur', 'Salle']
            ]
            
            for session in sessions_data:
                table_data.append([
                    session.get('jour', ''),
                    session.get('periode', ''),
                    f"{session.get('heure_debut', '')} - {session.get('heure_fin', '')}",
                    session.get('prof', ''),
                    session.get('salle', '')
                ])
            
            # Créer le tableau
            t = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 1.5*inch, 1*inch])
            t.setStyle(TableStyle([
                # En-tête
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Contenu
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1F2937')),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # Grille
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(t)
            story.append(Spacer(1, 0.4*inch))
        
        # Liste des étudiants
        if students_list:
            story.append(Paragraph(f"👥 Liste des étudiants ({len(students_list)})", styles['CustomSubtitle']))
            
            # Données du tableau des étudiants
            students_table_data = [['N°', 'Nom Complet', 'Téléphone']]
            
            for idx, student in enumerate(students_list, 1):
                students_table_data.append([
                    str(idx),
                    f"{student.get('nom', '')} {student.get('prenom', '')}",
                    student.get('tel', 'N/A')
                ])
            
            # Créer le tableau
            st = Table(students_table_data, colWidths=[0.5*inch, 3*inch, 2*inch])
            st.setStyle(TableStyle([
                # En-tête
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Contenu
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1F2937')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # Grille
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
            ]))
            
            story.append(st)
        
        # Pied de page
        story.append(Spacer(1, 0.5*inch))
        footer = f"<i>Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>"
        story.append(Paragraph(footer, styles['CustomNormal']))
        
        # Générer le PDF
        doc.build(story)
        
        return filepath
    
    # ========================
    # 2. FACTURE ÉLÈVE
    # ========================
    
    def generate_student_invoice(self, student_data, payment_data, school_info=None):
        """
        Génère une facture de paiement pour un élève
        
        Args:
            student_data: dict avec {id, nom, prenom, niveau, tel}
            payment_data: dict avec {montant, mois, annee, date_paiement, ref}
            school_info: dict optionnel avec {nom, adresse, tel, email}
        
        Returns:
            str: Chemin du fichier PDF généré
        """
        filename = f"facture_{student_data['nom']}_{payment_data['mois']}_{payment_data['annee']}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Créer le document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=50
        )
        
        story = []
        styles = self._get_styles()
        
        # Informations de l'établissement
        if school_info:
            school_header = f"""
            <b>{school_info.get('nom', 'Centre de Soutien Scolaire')}</b><br/>
            {school_info.get('adresse', '')}<br/>
            Tél: {school_info.get('tel', '')} | Email: {school_info.get('email', '')}
            """
            story.append(Paragraph(school_header, styles['CustomNormal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Titre
        story.append(Paragraph("💰 REÇU DE PAIEMENT", styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Numéro de référence
        ref_number = payment_data.get('ref', f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        story.append(Paragraph(f"<b>N° de Référence:</b> {ref_number}", styles['CustomNormal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informations élève
        story.append(Paragraph("📌 Informations de l'élève", styles['CustomSubtitle']))
        student_info = f"""
        <b>Nom:</b> {student_data['nom']} {student_data['prenom']}<br/>
        <b>Niveau:</b> {student_data.get('niveau', 'N/A')}<br/>
        <b>Téléphone:</b> {student_data.get('tel', 'N/A')}
        """
        story.append(Paragraph(student_info, styles['CustomNormal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Détails du paiement
        story.append(Paragraph("💵 Détails du paiement", styles['CustomSubtitle']))
        
        payment_table_data = [
            ['Description', 'Mois', 'Année', 'Montant'],
            [
                'Frais de scolarité',
                payment_data['mois'],
                str(payment_data['annee']),
                f"{payment_data['montant']} DH"
            ]
        ]
        
        pt = Table(payment_table_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1.5*inch])
        pt.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenu
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 1.5, colors.grey),
        ]))
        
        story.append(pt)
        story.append(Spacer(1, 0.3*inch))
        
        # Total
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['CustomNormal'],
            fontSize=14,
            textColor=colors.HexColor('#1E40AF'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        )
        story.append(Paragraph(f"<b>TOTAL À PAYER: {payment_data['montant']} DH</b>", total_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Date de paiement
        payment_date = payment_data.get('date_paiement', datetime.now().strftime('%d/%m/%Y'))
        story.append(Paragraph(f"<b>Date de paiement:</b> {payment_date}", styles['CustomNormal']))
        
        # Signature
        story.append(Spacer(1, 0.8*inch))
        signature_text = """
        <b>Signature et Cachet</b><br/>
        _______________________________
        """
        signature_style = ParagraphStyle(
            'SignatureStyle',
            parent=styles['CustomNormal'],
            alignment=TA_RIGHT
        )
        story.append(Paragraph(signature_text, signature_style))
        
        # Pied de page
        story.append(Spacer(1, 0.5*inch))
        footer = f"<i>Facture générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>"
        story.append(Paragraph(footer, styles['CustomNormal']))
        
        # Générer le PDF
        doc.build(story)
        
        return filepath
    
    # ========================
    # 3. FICHE DE PAIE PROFESSEUR
    # ========================
    
    def generate_teacher_payslip(self, teacher_data, work_data, school_info=None):
        """
        Génère une fiche de paie pour un professeur
        
        Args:
            teacher_data: dict avec {id, nom, prenom, matiere, tel, salaire_horaire}
            work_data: dict avec {mois, annee, heures_travaillees, sessions_list}
            school_info: dict optionnel avec {nom, adresse, tel}
        
        Returns:
            str: Chemin du fichier PDF généré
        """
        filename = f"fiche_paie_{teacher_data['nom']}_{work_data['mois']}_{work_data['annee']}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Créer le document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=50
        )
        
        story = []
        styles = self._get_styles()
        
        # Informations de l'établissement
        if school_info:
            school_header = f"""
            <b>{school_info.get('nom', 'Centre de Soutien Scolaire')}</b><br/>
            {school_info.get('adresse', '')}<br/>
            Tél: {school_info.get('tel', '')}
            """
            story.append(Paragraph(school_header, styles['CustomNormal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Titre
        story.append(Paragraph("📄 FICHE DE PAIE", styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Période
        period_text = f"<b>Période:</b> {work_data['mois']} {work_data['annee']}"
        story.append(Paragraph(period_text, styles['CustomNormal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informations professeur
        story.append(Paragraph("👨‍🏫 Informations de l'enseignant", styles['CustomSubtitle']))
        teacher_info = f"""
        <b>Nom:</b> {teacher_data['nom']} {teacher_data['prenom']}<br/>
        <b>Matière:</b> {teacher_data.get('matiere', 'N/A')}<br/>
        <b>Téléphone:</b> {teacher_data.get('tel', 'N/A')}<br/>
        <b>Taux horaire:</b> {teacher_data.get('salaire_horaire', 0)} DH/heure
        """
        story.append(Paragraph(teacher_info, styles['CustomNormal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Détails des heures travaillées
        story.append(Paragraph("⏱️ Détail des heures", styles['CustomSubtitle']))
        
        # Tableau des séances
        if 'sessions_list' in work_data and work_data['sessions_list']:
            sessions_table_data = [['Date', 'Groupe', 'Horaire', 'Heures']]
            
            for session in work_data['sessions_list']:
                sessions_table_data.append([
                    session.get('date', ''),
                    session.get('groupe', ''),
                    f"{session.get('heure_debut', '')} - {session.get('heure_fin', '')}",
                    str(session.get('heures', 0))
                ])
            
            st = Table(sessions_table_data, colWidths=[1.5*inch, 2*inch, 1.8*inch, 1*inch])
            st.setStyle(TableStyle([
                # En-tête
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Contenu
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1F2937')),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # Grille
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white]),
            ]))
            
            story.append(st)
            story.append(Spacer(1, 0.3*inch))
        
        # Calcul du salaire
        story.append(Paragraph("💰 Calcul du salaire", styles['CustomSubtitle']))
        
        heures_travaillees = work_data.get('heures_travaillees', 0)
        salaire_horaire = teacher_data.get('salaire_horaire', 0)
        salaire_brut = heures_travaillees * salaire_horaire
        
        salary_table_data = [
            ['Description', 'Détail', 'Montant (DH)'],
            ['Heures travaillées', f"{heures_travaillees} h", ''],
            ['Taux horaire', f"{salaire_horaire} DH/h", ''],
            ['SALAIRE BRUT', '', f"{salaire_brut:.2f} DH"]
        ]
        
        slt = Table(salary_table_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        slt.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Lignes normales
            ('BACKGROUND', (0, 1), (-1, 2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, 2), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 1), (1, 2), 'LEFT'),
            ('ALIGN', (2, 1), (2, 2), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, 2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, 2), 10),
            
            # Ligne total
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#FEF3C7')),
            ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#1E40AF')),
            ('ALIGN', (0, 3), (-1, 3), 'CENTER'),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (-1, 3), 12),
            ('TOPPADDING', (0, 3), (-1, 3), 12),
            ('BOTTOMPADDING', (0, 3), (-1, 3), 12),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 1.5, colors.grey),
        ]))
        
        story.append(slt)
        story.append(Spacer(1, 0.5*inch))
        
        # Signature
        signature_text = """
        <b>Signature de l'établissement</b><br/>
        <br/>
        _______________________________
        """
        signature_style = ParagraphStyle(
            'SignatureStyle',
            parent=styles['CustomNormal'],
            alignment=TA_RIGHT
        )
        story.append(Paragraph(signature_text, signature_style))
        
        # Pied de page
        story.append(Spacer(1, 0.5*inch))
        footer = f"<i>Fiche générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>"
        story.append(Paragraph(footer, styles['CustomNormal']))
        
        # Générer le PDF
        doc.build(story)
        
        return filepath


# Fonction utilitaire pour tester le module
if __name__ == "__main__":
    generator = PDFGenerator()
    
    # Test 1: Emploi du temps
    group_data = {
        'nom': 'Groupe Math TC',
        'matiere': 'Mathématiques',
        'niveau': 'Tronc Commun'
    }
    sessions = [
        {'jour': 'Lundi', 'periode': 'Matin', 'heure_debut': '09:00', 'heure_fin': '11:00', 'prof': 'Ahmed Alami', 'salle': 'Salle A'},
        {'jour': 'Mercredi', 'periode': 'Après-midi', 'heure_debut': '14:00', 'heure_fin': '16:00', 'prof': 'Ahmed Alami', 'salle': 'Salle B'}
    ]
    students = [
        {'nom': 'Bennani', 'prenom': 'Youssef', 'tel': '0612345678'},
        {'nom': 'Alami', 'prenom': 'Fatima', 'tel': '0623456789'}
    ]
    
    print("✅ Test emploi du temps...")
    schedule_pdf = generator.generate_group_schedule(group_data, sessions, students)
    print(f"   Généré: {schedule_pdf}")
    
    # Test 2: Facture élève
    student = {
        'nom': 'Bennani',
        'prenom': 'Youssef',
        'niveau': 'Tronc Commun',
        'tel': '0612345678'
    }
    payment = {
        'montant': 500,
        'mois': 'Janvier',
        'annee': 2024,
        'date_paiement': '15/01/2024',
        'ref': 'REF-2024010001'
    }
    
    print("✅ Test facture élève...")
    invoice_pdf = generator.generate_student_invoice(student, payment)
    print(f"   Généré: {invoice_pdf}")
    
    # Test 3: Fiche de paie professeur
    teacher = {
        'nom': 'Alami',
        'prenom': 'Ahmed',
        'matiere': 'Mathématiques',
        'tel': '0634567890',
        'salaire_horaire': 120
    }
    work = {
        'mois': 'Janvier',
        'annee': 2024,
        'heures_travaillees': 40,
        'sessions_list': [
            {'date': '08/01/2024', 'groupe': 'TC Math', 'heure_debut': '09:00', 'heure_fin': '11:00', 'heures': 2},
            {'date': '10/01/2024', 'groupe': 'TC Math', 'heure_debut': '14:00', 'heure_fin': '16:00', 'heures': 2}
        ]
    }
    
    print("✅ Test fiche de paie professeur...")
    payslip_pdf = generator.generate_teacher_payslip(teacher, work)
    print(f"   Généré: {payslip_pdf}")
    
    print("\n🎉 Tous les tests sont réussis!")
