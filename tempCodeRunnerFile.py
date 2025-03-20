    if self.text == "Output":
            # Check if the connection exists
            if self.input_sockets[0].connection and self.input_sockets[0].connection.start_socket:
                # Process the input and produce output
                start_socket = self.input_sockets[0].connection.start_socket
                start_node = start_socket.parentItem()
                
                print(f"Start socket: {start_socket}")
                print(f"Start node: {start_node}")
                print(f"Start node type: {start_node.text if start_node else 'None'}")
                
                if start_node:
                    if start_node.text == "Input" and start_node.input_field:
                        # For Input nodes, use the value from the input field
                        input_value = start_node.input_field.text()
                        print(f"Output Node Value from Input: {input_value}")
                    elif start_node.text in ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]:
                        # For logic gates, we would recursively process them
                        # This is a placeholder for the actual logic processing
                        print(f"Processing logic gate: {start_node.text}")
                        # Here you would call process() on the start_node
                        # and use its result
                        if start_node.text == "NOT":
                            # Example for NOT gate (assuming binary values)
                            print(f"Output Node Value from NOT: 0")  # Simple placeholder
                        else:
                            print(f"Output Node Value from {start_node.text}: 1")  # Simple placeholder
                    else:
                        print(f"Connected to {start_node.text}, but processing not implemented")
                else:
                    print("No valid input to process")
            else:
                print("No connection to process")
    