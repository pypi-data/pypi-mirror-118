from graph import Graph


if __name__ == "__main__":
    documents = [
        {
            "title": "Article 1",
            "authors": [
                {"name": "annie"},
                {"name": "val"},
                {"name": "chris"}
            ]
        },
        {
            "title": "Article 2",
            "authors": [
                {"name": "annie"},
                {"name": "val"}
            ]
        },
        {
            "authors": [
                {"name": "ian"},
                {"name": "hamsa"}
            ]
        },
        {
            "authors": [
                {"name": "ian"},
                {"name": "virisha"}
            ]
        }

    ]

    ar_graph = Graph()
    ar_graph.fit(
        documents=documents,  # limit to a small number of documents
        progress_bar=True,  # use a progress bar to indicate how far along processing is
        authorship_key="authors",
        keys=set(["name"]),
    )