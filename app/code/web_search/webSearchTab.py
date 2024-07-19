import panel as pn

import web_search.webSearchAgent as wsa

def webSearch():
    colWidth = 500

    # Input widgets
    queryInput = pn.widgets.TextInput(name="Search query",
                                      placeholder="Enter search query here",
                                      width=colWidth)
    
    numBullets = pn.widgets.IntSlider(name="Number of bullets in summary",
                                      start=1, end=20, value=4,
                                      width=colWidth)

    numRefinements = pn.widgets.IntSlider(name=("Number of additional " +
                                               "questions to generate"),
                                          start=0, end=5, value=2,
                                          width=colWidth)

    searchButton = pn.widgets.Button(name="Start search", margin=35)

    # Get agent
    graph = wsa.getWebSearchGraph()

    # Output panes
    def resultPane(results: str|None, sufficient: str):
        """Update result pane."""
        if results == "":
            resStr = "## Results are posted here."
        else:
            resStr = (f"## Summary \n The model deemed the summary " +
                      f"{sufficient} \n\n {results}")

        return pn.Card(pn.pane.Markdown(resStr, width=int(colWidth*0.9),
                                        height=colWidth//2),
                                        collapsed=False, scroll=True,
                                        collapsible=False, width=colWidth,
                                        height=colWidth//2)

    def sourcePane(results: str|None):
        """Update Source pane."""
        if results == "":
            resStr = "## Sources are posted here."
        else:
            resStr = f"## Sources \n\n {results}"

        return pn.Card(pn.pane.Markdown(resStr, width=int(colWidth*0.9),
                                        height=colWidth//3), 
                                        collapsed=False, scroll=True,
                                        collapsible=False, width=colWidth, 
                                        height=colWidth//3)
    
    def enhancedPane(results: str|None):
        """Update enhanced pane with generated questions."""
        if results == "":
            resStr = "## Enhanced questions are posted here."
        else:
            resStr = f"## Enhanced questions \n\n {results}"

        return pn.Card(pn.pane.Markdown(resStr, width=int(colWidth*0.9),
                                        height=colWidth//3), 
                                        collapsed=False, scroll=True,
                                        collapsible=False, width=colWidth, 
                                        height=colWidth//3)
    
    def searchSummarize(query: str|None, nBullets: int, nRefinements:int,
                        run):
        """Make search query and update result panes.

        Args:
            query (str | None): The user provided query
            nBullets (int): Number of bullet points for summary
            nRefinements (int): Number of generated questions for search.
            run: the event used to trigger the function.

        Returns:
            pn.Column: column containing result panes.
        """
        if query!="":
            finalState = graph.invoke({"question": query, 
                                   "nPoints": nBullets,
                                   "nQuestions":nRefinements,
                                   "maxIters":3, "iter":0})
            resStr = finalState["generation"]
            enhancedStr = "\n".join(["• " + q for q in 
                                     finalState["enhancedQuestions"]])
            sourcesStr = "\n".join(["• " + x.split("]")[0] for x in 
                          finalState["webSearch"].split("link: ")[1:]])
            sufficientStr = finalState["graded"]
        else:
            resStr = ""
            enhancedStr = ""
            sourcesStr = ""
            sufficientStr = ""
        
        res = resultPane(resStr, sufficientStr)
        
        enhanced = enhancedPane(str(enhancedStr))

        sources = sourcePane(sourcesStr)

        return pn.Column(res, enhanced, sources)
    
    # Bind to search button
    results = pn.bind(lambda x: searchSummarize(queryInput.value,
                                                numBullets.value,
                                                numRefinements.value,
                                                x), searchButton)

    # Static panes
    graphImg = pn.pane.SVG("/code/app/imgs/webSearch.drawio.svg")

    return pn.Row(pn.Column(queryInput,
                            numBullets,
                            numRefinements,
                            results,
                            ), searchButton, graphImg)



