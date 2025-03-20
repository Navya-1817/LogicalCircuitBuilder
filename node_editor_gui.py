from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QTabWidget, QFileDialog, QWidget, QVBoxLayout, QListWidget, QSplitter, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsProxyWidget, QPushButton
from PyQt5.QtCore import Qt, QRectF, QMimeData, QPointF, QLineF
from PyQt5.QtGui import QBrush, QPen, QPainter, QDrag, QColor
import sys

class NodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor")
        self.setGeometry(100, 100, 1000, 600)
        
        # For undo/redo functionality
        self.command_history = []
        self.redo_history = []
        self.clipboard = None
        self.current_theme = "Light"  # Default theme
        
        # Add status bar
        self.status_bar = self.statusBar()
        
        self.initUI()
    
    def execute_command(self, command):
        command.execute()
        self.command_history.append(command)
        self.redo_history.clear()  # Clear redo history after a new command

    def undo(self):
        if self.command_history:
            command = self.command_history.pop()
            command.undo()
            self.redo_history.append(command)
            self.status_bar.showMessage(f"Undo: {command}", 2000)

    def redo(self):
        if self.redo_history:
            command = self.redo_history.pop()
            command.execute()
            self.command_history.append(command)
            self.status_bar.showMessage(f"Redo: {command}", 2000)

    def initUI(self):
        # Create Menu Bar
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        file_menu.addActions([new_action, open_action, save_action, exit_action])
        
        new_action.triggered.connect(self.new_tab)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)
        
        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Shift+Z")
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        
        edit_menu.addActions([undo_action, redo_action])
        edit_menu.addSeparator()
        edit_menu.addActions([cut_action, copy_action, paste_action, delete_action])
        
        # Connect edit actions
        undo_action.triggered.connect(self.undo)
        redo_action.triggered.connect(self.redo)
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        delete_action.triggered.connect(self.delete_selected)
        
        # Window Menu
        window_menu = menubar.addMenu("Window")
        light_theme_action = QAction("Light Theme", self)
        dark_theme_action = QAction("Dark Theme", self)
        blue_theme_action = QAction("Blue Theme", self)
        green_theme_action = QAction("Green Theme", self)
        
        window_menu.addActions([light_theme_action, dark_theme_action, blue_theme_action, green_theme_action])
        
        # Connect window actions
        light_theme_action.triggered.connect(lambda: self.change_theme("Light"))
        dark_theme_action.triggered.connect(lambda: self.change_theme("Dark"))
        blue_theme_action.triggered.connect(lambda: self.change_theme("Blue"))
        green_theme_action.triggered.connect(lambda: self.change_theme("Green"))
        
        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        
        # Splitter for Side Panel and Main Tab Widget
        splitter = QSplitter(Qt.Horizontal)
        
        # Side Panel (Node List)
        self.node_list = NodeList()
        splitter.addWidget(self.node_list)
        
        # Main Area (Tabbed Interface)
        self.tab_widget = QTabWidget()
        splitter.addWidget(self.tab_widget)
        splitter.setStretchFactor(1, 3)
        
        layout.addWidget(splitter)
        self.central_widget.setLayout(layout)
        
        # Create a default tab
        self.new_tab()
    
    def new_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        scene = NodeGraphicsScene(self)
        view = QGraphicsView(scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setSceneRect(-5000, -5000, 10000, 10000)
        tab.scene = scene  # Store scene reference in tab
        tab.view = view  # Store view reference in tab
        layout.addWidget(view)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "New Tab")
    
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            print(f"Opened file: {file_name}")
            self.status_bar.showMessage(f"Opened file: {file_name}", 2000)
    
    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File")
        if file_name:
            print(f"Saved file: {file_name}")
            self.status_bar.showMessage(f"Saved file: {file_name}", 2000)
    
    # Edit menu functions
    def undo(self):
        if self.command_history:
            command = self.command_history.pop()
            self.redo_history.append(command)
            print(f"Undo: {command}")
            # Here you would implement the actual undo functionality
            self.status_bar.showMessage("Undo operation", 2000)
    
    def redo(self):
        if self.redo_history:
            command = self.redo_history.pop()
            self.command_history.append(command)
            print(f"Redo: {command}")
            # Here you would implement the actual redo functionality
            self.status_bar.showMessage("Redo operation", 2000)
    
    def cut(self):
        selected_items = self.get_selected_items()
        if selected_items:
            self.clipboard = selected_items
            self.delete_selected()
            self.status_bar.showMessage("Cut items to clipboard", 2000)
    
    def copy(self):
        selected_items = self.get_selected_items()
        if selected_items:
            self.clipboard = selected_items
            self.status_bar.showMessage("Copied items to clipboard", 2000)
    
    def paste(self):
        if self.clipboard:
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                scene = current_tab.scene
                for item_data in self.clipboard:
                    # Create a new node based on clipboard data
                    new_node = NodeItem(
                        item_data['x'] + 20,  # Offset to make it visible
                        item_data['y'] + 20,  # Offset to make it visible
                        item_data['text']
                    )
                    scene.addItem(new_node)
                self.status_bar.showMessage("Pasted items from clipboard", 2000)
    
    def delete_selected(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            scene = current_tab.scene
            selected_items = [item for item in scene.selectedItems() if isinstance(item, NodeItem)]
            for item in selected_items:
                # Remove all connections
                for socket in item.input_sockets:
                    if socket.connection:
                        if isinstance(socket.connection, ConnectionLine):
                            scene.removeItem(socket.connection)
                        socket.connection = None
                
                # Remove output connections
                if item.output_socket and item.output_socket.connection:
                    if isinstance(item.output_socket.connection, ConnectionLine):
                        scene.removeItem(item.output_socket.connection)
                    item.output_socket.connection = None
                
                # Remove the node
                scene.removeItem(item)
            
            self.status_bar.showMessage(f"Deleted {len(selected_items)} items", 2000)
    
    def get_selected_items(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            scene = current_tab.scene
            selected_items = []
            for item in scene.selectedItems():
                if isinstance(item, NodeItem):
                    # Store relevant data for copying
                    item_data = {
                        'x': item.x(),
                        'y': item.y(),
                        'text': item.text,
                    }
                    selected_items.append(item_data)
            return selected_items
        return []
    
    # Window menu functions
    def change_theme(self, theme):
        self.current_theme = theme
        
        # Apply theme to all tabs and scenes
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            view = tab.view
            scene = tab.scene
            
            # Set scene background color based on theme
            if theme == "Light":
                scene.setBackgroundBrush(QBrush(Qt.white))
            elif theme == "Dark":
                scene.setBackgroundBrush(QBrush(Qt.black))
            elif theme == "Blue":
                scene.setBackgroundBrush(QBrush(QColor(200, 210, 255)))
            elif theme == "Green":
                scene.setBackgroundBrush(QBrush(QColor(200, 255, 210)))
        
        # Apply theme to UI elements
        self.status_bar.showMessage(f"Theme changed to {theme}", 2000)

class ConnectionLine(QGraphicsItem):
    def __init__(self, start_socket, end_socket=None):
        super().__init__()
        self.start_socket = start_socket
        self.end_socket = end_socket or start_socket.scenePos()
        self.setZValue(-1)
    
    def boundingRect(self):
        start_pos = self.mapFromScene(self.start_socket.scenePos()) if isinstance(self.start_socket, QGraphicsItem) else self.start_socket
        end_pos = self.mapFromScene(self.end_socket.scenePos()) if isinstance(self.end_socket, QGraphicsItem) else self.end_socket
        return QRectF(start_pos, end_pos).normalized().adjusted(-10, -10, 10, 10)
    
    def paint(self, painter, option, widget):
        start_pos = self.start_socket.scenePos() if isinstance(self.start_socket, QGraphicsItem) else self.start_socket
        end_pos = self.end_socket.scenePos() if isinstance(self.end_socket, QGraphicsItem) else self.end_socket
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(QLineF(start_pos, end_pos))
        
    def removeFromSockets(self):
        """Remove this connection from its sockets"""
        if isinstance(self.start_socket, Socket):
            if self.start_socket.connection == self:
                self.start_socket.connection = None
        if isinstance(self.end_socket, Socket):
            if self.end_socket.connection == self:
                self.end_socket.connection = None

class Socket(QGraphicsItem):
    def __init__(self, parent, is_input=True, index=0):
        super().__init__(parent)
        self.parent_item = parent
        self.is_input = is_input
        self.index = index
        self.radius = 6
        self.setPos(self.socket_position())
        self.connection = None
    
    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
    
    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.blue if self.is_input else Qt.red))
        painter.drawEllipse(self.boundingRect())
    
    def socket_position(self):
        y_offset = 15 + self.index * 15
        return QPointF(-self.radius if self.is_input else self.parent_item.width + self.radius, y_offset)
    
    def mousePressEvent(self, event):
        if not self.is_input:
            self.connection = ConnectionLine(self)
            self.scene().addItem(self.connection)
    
    def mouseMoveEvent(self, event):
        if self.connection:
            pos = event.scenePos()
            self.connection.prepareGeometryChange()
            self.connection.end_socket = pos
            self.scene().update()

    def mouseReleaseEvent(self, event):
        if not self.connection:
            return

        items = self.scene().items(event.scenePos())
        for item in items:
            if isinstance(item, Socket) and item.is_input and item != self:
                # Make connection
                self.connection.end_socket = item
                item.connection = self.connection
                self.scene().update()

                # Call process method if connecting to Output or Write Output node
                if item.parentItem() and item.parentItem().text in ["Output", "Write Output"]:
                    print(f"Connected to {item.parentItem().text} node, processing...")
                    item.parentItem().process()
                return

        # If we reach here, no valid socket was found at release position
        if self.connection:
            self.scene().removeItem(self.connection)
            self.connection = None

class NodeItem(QGraphicsItem):
    def __init__(self, x, y, text):
        super().__init__()
        self.text = text
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)
        
        self.width = 120
        self.height = 70 if text == "Write Output" else 50
        self.input_field = None
        self.output_value = None

        if text == "Input":
            self.input_field = QLineEdit()
            self.input_field.setFixedWidth(100)
            self.input_field.setText("1")
            self.input_field.textChanged.connect(self.on_input_changed)  # Connect signal
            self.input_proxy = QGraphicsProxyWidget(self)
            self.input_proxy.setWidget(self.input_field)
            self.input_proxy.setPos(10, 20)
        elif text == "Output":
            self.output_field = QLineEdit()
            self.output_field.setFixedWidth(100)
            self.output_field.setReadOnly(True)
            self.output_field.setText("--")
            self.output_proxy = QGraphicsProxyWidget(self)
            self.output_proxy.setWidget(self.output_field)
            self.output_proxy.setPos(10, 20)
        elif text == "Write Output":
            self.output_field = QLineEdit()
            self.output_field.setFixedWidth(100)
            self.output_field.setReadOnly(True)
            self.output_field.setText("--")
            self.output_proxy = QGraphicsProxyWidget(self)
            self.output_proxy.setWidget(self.output_field)
            self.output_proxy.setPos(10, 20)
            self.write_button = QPushButton("Write")
            self.write_button.setFixedWidth(100)
            self.write_proxy = QGraphicsProxyWidget(self)
            self.write_proxy.setWidget(self.write_button)
            self.write_proxy.setPos(10, 50)
            self.write_button.clicked.connect(self.write_to_file)

        if text in ["Output", "Write Output"]:
            self.input_sockets = [Socket(self, is_input=True, index=0)]
        else:
            self.input_sockets = [Socket(self, is_input=True, index=i) for i in range(2 if text not in ["NOT", "Input"] else 1)]
        
        self.output_socket = Socket(self, is_input=False)

    def on_input_changed(self):
        # Trigger processing for connected nodes
        if self.output_socket and self.output_socket.connection:
            connected_node = self.output_socket.connection.end_socket.parentItem()
            if connected_node:
                connected_node.process()

    def process(self):
        if self.text in ["Output", "Write Output"]:
            if self.input_sockets[0].connection and self.input_sockets[0].connection.start_socket:
                start_socket = self.input_sockets[0].connection.start_socket
                start_node = start_socket.parentItem()
                if start_node:
                    if start_node.text == "Input" and start_node.input_field:
                        input_value = start_node.input_field.text().strip()
                        if input_value in ["0", "1"]:
                            self.output_field.setText(input_value)
                            self.output_value = input_value
                        else:
                            self.output_field.setText("Use 0/1")
                    elif start_node.text in ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]:
                        result = self.process_logic_gate(start_node)
                        if result is not None:
                            self.output_field.setText(result)
                            self.output_value = result
                        else:
                            self.output_field.setText("Error")
                    else:
                        self.output_field.setText("Error")
                else:
                    self.output_field.setText("Error")
            else:
                self.output_field.setText("No input")

    def write_to_file(self):
        if self.output_field and self.output_field.text() != "--":
            file_name, _ = QFileDialog.getSaveFileName(None, "Save Output", "", "Text Files (*.txt)")
            if file_name:
                with open(file_name, "w") as file:
                    file.write(self.output_field.text())
                print(f"Output written to {file_name}")

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black))
        painter.drawRect(self.boundingRect())
        painter.drawText(10, 15, self.text)

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete_action = menu.addAction("Delete Node")
        action = menu.exec_(event.screenPos())
        
        if action == delete_action:
            # Remove all connections
            for socket in self.input_sockets:
                if socket.connection:
                    if isinstance(socket.connection, ConnectionLine):
                        self.scene().removeItem(socket.connection)
                    socket.connection = None
            
            # Remove the connection from the output socket
            if hasattr(self, 'output_socket') and self.output_socket and self.output_socket.connection:
                if isinstance(self.output_socket.connection, ConnectionLine):
                    self.scene().removeItem(self.output_socket.connection)
                self.output_socket.connection = None
                
            # Remove the node itself
            command = DeleteNodeCommand(self.scene(), self)
            self.scene().parent().execute_command(command)
       

    def process_logic_gate(self, gate_node):
        """Process a logic gate node and return its output value"""
        
        gate_type = gate_node.text
        
        # For NOT gate (1 input)
        if gate_type == "NOT":
            # Check if the NOT gate has an input connection
            if gate_node.input_sockets[0].connection and gate_node.input_sockets[0].connection.start_socket:
                input_source = gate_node.input_sockets[0].connection.start_socket.parentItem()
                
                # Get input value (recursively if needed)
                input_value = self.get_node_value(input_source)
                if input_value in ["0", "1"]:
                    # NOT operation: invert the input
                    return "1" if input_value == "0" else "0"
            return None
            
        # For all other gates (2 inputs)
        elif gate_type in ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]:
            # Check if both inputs have connections
            if (len(gate_node.input_sockets) >= 2 and 
                gate_node.input_sockets[0].connection and gate_node.input_sockets[0].connection.start_socket and
                gate_node.input_sockets[1].connection and gate_node.input_sockets[1].connection.start_socket):
                
                # Get the input sources
                input_source1 = gate_node.input_sockets[0].connection.start_socket.parentItem()
                input_source2 = gate_node.input_sockets[1].connection.start_socket.parentItem()
                
                # Get input values (recursively if needed)
                input1 = self.get_node_value(input_source1)
                input2 = self.get_node_value(input_source2)
                
                # Process based on gate type
                if input1 in ["0", "1"] and input2 in ["0", "1"]:
                    if gate_type == "AND":
                        result = "1" if input1 == "1" and input2 == "1" else "0"
                    elif gate_type == "OR":
                        result = "1" if input1 == "1" or input2 == "1" else "0"
                    elif gate_type == "NAND":
                        result = "0" if input1 == "1" and input2 == "1" else "1"
                    elif gate_type == "NOR":
                        result = "0" if input1 == "1" or input2 == "1" else "1"
                    elif gate_type == "XOR":
                        result = "1" if input1 != input2 else "0"
                    elif gate_type == "XNOR":
                        result = "1" if input1 == input2 else "0"
                    return result
            return None
        
        return None

    def get_node_value(self, node):
        """Get the output value from a node, recursively processing if needed"""
        if not node:
            return None
            
        # For Input nodes, get value directly from the input field
        if node.text == "Input" and node.input_field:
            value = node.input_field.text().strip()
            return value if value in ["0", "1"] else None
            
        # For logic gates, recursively process the gate
        elif node.text in ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]:
            return self.process_logic_gate(node)
            
        # Default case
        return None

class NodeGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 20  # Size of the grid squares
        self.grid_color = QColor(200, 200, 200)  # Light gray grid lines

    def dropEvent(self, event):
        text = event.mimeData().text()
        pos = event.scenePos()
        command = AddNodeCommand(self, text, pos.x(), pos.y())
        self.parent().execute_command(command)
        event.acceptProposedAction()

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # Draw the grid
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        lines = []
        for x in range(left, int(rect.right()), self.grid_size):
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))
        for y in range(top, int(rect.bottom()), self.grid_size):
            lines.append(QLineF(rect.left(), y, rect.right(), y))

        painter.setPen(QPen(self.grid_color, 1))
        painter.drawLines(lines)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        text = event.mimeData().text()
        pos = event.scenePos()
        node = NodeItem(pos.x(), pos.y(), text)
        self.addItem(node)
        event.acceptProposedAction()

class NodeList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["Input", "Output", "AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR","Write Output"])
        self.setDragEnabled(True)
    
    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(item.text())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        
class Command:
    def __init__(self, description):
        self.description = description

    def execute(self):
        pass

    def undo(self):
        pass

    def __str__(self):
        return self.description
    
class AddNodeCommand(Command):
    def __init__(self, scene, node_type, pos_x, pos_y):
        super().__init__(f"Add {node_type} node")
        self.scene = scene
        self.node_type = node_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.node = None

    def execute(self):
        self.node = NodeItem(self.pos_x, self.pos_y, self.node_type)
        self.scene.addItem(self.node)

    def undo(self):
        if self.node:
            self.scene.removeItem(self.node)

    def redo(self):
        self.execute()

class DeleteNodeCommand(Command):
    def __init__(self, scene, node):
        super().__init__(f"Delete {node.text} node")
        self.scene = scene
        self.node = node
        self.connections = []

    def execute(self):
        # Store connections for undo
        for socket in self.node.input_sockets:
            if socket.connection:
                self.connections.append({
                    'connection': socket.connection,
                    'start_socket': socket.connection.start_socket,
                    'end_socket': socket.connection.end_socket
                })
                self.scene.removeItem(socket.connection)
                socket.connection = None

        if self.node.output_socket and self.node.output_socket.connection:
            self.connections.append({
                'connection': self.node.output_socket.connection,
                'start_socket': self.node.output_socket.connection.start_socket,
                'end_socket': self.node.output_socket.connection.end_socket
            })
            self.scene.removeItem(self.node.output_socket.connection)
            self.node.output_socket.connection = None

        # Remove the node
        self.scene.removeItem(self.node)

    def undo(self):
        # Restore the node
        self.scene.addItem(self.node)

        # Restore connections
        for conn in self.connections:
            conn['connection'].start_socket = conn['start_socket']
            conn['connection'].end_socket = conn['end_socket']
            self.scene.addItem(conn['connection'])

    def redo(self):
        # Re-execute the deletion
        self.execute()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NodeEditor()
    window.show()
    sys.exit(app.exec_())