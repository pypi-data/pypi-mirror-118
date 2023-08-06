import qdarkstyle

DarkStyle = qdarkstyle.load_stylesheet(qt_api='pyqt5')
DarkStyle = DarkStyle.replace('''QSplitter {
  background-color: #455364;
  spacing: 0px;
  padding: 0px;
  margin: 0px;
}

QSplitter::handle {
  background-color: #455364;
  border: 0px solid #19232D;
  spacing: 0px;
  padding: 1px;
  margin: 0px;
}
''', '''
QSplitter {
  background-color: #00000000;
  spacing: 0px;
  padding: 0px;
  margin: 0px;
}

QSplitter::handle {
  background-color: #00000000;
  border: 0px solid #19232D;
  spacing: 0px;
  padding: 1px;
  margin: 0px;
}''')

DarkStyle = DarkStyle.replace('''
QGroupBox::title {
  subcontrol-origin: margin;
  subcontrol-position: top left;
  left: 4px;
  padding-left: 2px;
  padding-right: 4px;
  padding-top: -4px;
}
''', '''
QGroupBox::title {
  subcontrol-origin: margin;
  subcontrol-position: top left;
  left: 4px;
  padding-left: 2px;
  padding-right: 4px;
  padding-top: -1px;
}
''')

DarkStyle = DarkStyle.replace(
'''
QDockWidget {
''',
'''
QDockWidget {
    font-size: 10pt;
'''
)

DarkStyle = DarkStyle.replace('* {',
'''
* {
  font-size: 9pt;
''')
