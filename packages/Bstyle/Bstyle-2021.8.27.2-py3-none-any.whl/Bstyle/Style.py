import qdarkstyle

DarkStyle = qdarkstyle.load_stylesheet(qt_api='pyqt5')
DarkStyle = DarkStyle.replace('''QSplitter {
  background-color: #32414B;
  spacing: 0px;
  padding: 0px;
  margin: 0px;
}

QSplitter::handle {
  background-color: #32414B;
  border: 0px solid #19232D;
  spacing: 0px;
  padding: 1px;
  margin: 0px;
}

QSplitter::handle:hover {
  background-color: #787878;
}

QSplitter::handle:horizontal {
  width: 5px;
  image: url(":/qss_icons/rc/line_vertical.png");
}

QSplitter::handle:vertical {
  height: 5px;
  image: url(":/qss_icons/rc/line_horizontal.png");
}''', '''
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
}

QSplitter::handle:hover {
  background-color: #787878;
}

QSplitter::handle:horizontal {
  width: 5px;
  image: url(":/qss_icons/rc/line_vertical.png");
}

QSplitter::handle:vertical {
  height: 5px;
  image: url(":/qss_icons/rc/line_horizontal.png");
}''')