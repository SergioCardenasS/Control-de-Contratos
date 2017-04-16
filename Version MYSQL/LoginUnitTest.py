#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt,QTimer
from views.login import login_window

app = QApplication(sys.argv)

class loginTest(unittest.TestCase):
	def setUp(self):
		self.form = login_window()

	def timeOut(self):
		allToplevelWidgets = QApplication.topLevelWidgets();
		a = False
		for w in allToplevelWidgets:
			if (w.inherits("QMessageBox")):
				QTest.keyClick(w, Qt.Key_Enter)
				a= True
		self.assertEqual(a,True)

	def test_combo(self):
		self.assertEqual(self.form.editUser.count(),8)
		self.assertEqual(self.form.editUser.itemText(0), "Control")
		self.assertEqual(self.form.editUser.itemText(1), "Comercial")
		self.assertEqual(self.form.editUser.itemText(2), "Abastecimientos")
		self.assertEqual(self.form.editUser.itemText(3), "Desarrollo")
		self.assertEqual(self.form.editUser.itemText(4), "Ingenieria")
		self.assertEqual(self.form.editUser.itemText(5), "Planificacion")
		self.assertEqual(self.form.editUser.itemText(6), "Logistica")
		self.assertEqual(self.form.editUser.itemText(7), "Control de Calidad")

	def test_bad_password(self):
		self.form.editPassword.setText("BAD PASSWORD")
		self.timer = QTimer(self.form)
		self.timer.setSingleShot(True)
		self.timer.singleShot(1000, self.timeOut)
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)

	def test_good_password_control(self):
		self.form.editUser.setCurrentIndex(0);
		self.form.editPassword.setText("Control")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_comercial(self):
		self.form.editUser.setCurrentIndex(1);
		self.form.editPassword.setText("Comercial")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_abastecimientos(self):
		self.form.editUser.setCurrentIndex(2);
		self.form.editPassword.setText("Abastecimientos")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_desarrollo(self):
		self.form.editUser.setCurrentIndex(3);
		self.form.editPassword.setText("Desarrollo")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_ingenieria(self):
		self.form.editUser.setCurrentIndex(4);
		self.form.editPassword.setText("Ingenieria")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_planificacion(self):
		self.form.editUser.setCurrentIndex(5);
		self.form.editPassword.setText("Planificacion")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_logistica(self):
		self.form.editUser.setCurrentIndex(6);
		self.form.editPassword.setText("Logistica")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

	def test_good_password_calidad(self):
		self.form.editUser.setCurrentIndex(7);
		self.form.editPassword.setText("Calidad")
		QTest.mouseClick(self.form.ingresarBoton, Qt.LeftButton)
		self.assertEqual(self.form.isVisible(),False)

if __name__ == "__main__":
    unittest.main()