import tkinter as tk
from tkinter import filedialog


class AIGUI:
    def __init__(self, master, processing_service, analysis_service):
        self.master = master
        self.processing_service = processing_service
        self.analysis_service = analysis_service
        master.title("AI Local Explorer")

        self.label = tk.Label(master, text="Welcome to AI Local Explorer")
        self.label.pack()

        self.process_button = tk.Button(
            master, text="Process File", command=self.process_file
        )
        self.process_button.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search)
        self.search_button.pack()

        self.visualize_button = tk.Button(
            master, text="Visualize Graph", command=self.visualize_graph
        )
        self.visualize_button.pack()

        self.cluster_button = tk.Button(
            master, text="Show Clusters", command=self.show_clusters
        )
        self.cluster_button.pack()

    def process_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.processing_service.process_file(file_path)
            tk.messagebox.showinfo(
                "Success", f"File {file_path} processed successfully!"
            )

    def search(self):
        query = tk.simpledialog.askstring("Search", "Enter your search query:")
        if query:
            results = self.analysis_service.search(
                query, self.processing_service.embedding_service
            )
            result_window = tk.Toplevel(self.master)
            result_window.title("Search Results")
            for file_path, similarity in results:
                tk.Label(
                    result_window,
                    text=f"File: {file_path}, Similarity: {similarity:.4f}",
                ).pack()

    def visualize_graph(self):
        self.analysis_service.visualize_graph()

    def show_clusters(self):
        cluster_info = self.analysis_service.get_cluster_info()
        cluster_window = tk.Toplevel(self.master)
        cluster_window.title("Document Clusters")
        for cluster, files in cluster_info.items():
            tk.Label(cluster_window, text=f"Cluster {cluster}:").pack()
            for file in files:
                tk.Label(cluster_window, text=f"  - {file}").pack()
            tk.Label(cluster_window, text="").pack()  # Empty label for spacing


def start_gui(processing_service, analysis_service):
    root = tk.Tk()
    gui = AIGUI(root, processing_service, analysis_service)
    root.mainloop()
