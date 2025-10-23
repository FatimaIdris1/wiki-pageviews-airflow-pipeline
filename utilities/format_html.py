def format_results_as_html(**kwargs):
    """
    Convert SQL results into a styled HTML table for email.
    """
    ti = kwargs['ti']  # Task instance from context
    results = ti.xcom_pull(task_ids='simple_analysis')

    if not results:
        html = "<h3>DAG Succeeded!</h3><p>No results found.</p>"
    else:
        headers = ["Project", "Page Title", "Views", "Response Size"]

        html = """
        <h3>DAG Succeeded!</h3>
        <p>Here are the top pages by views:</p>
        <table border="1" cellspacing="0" cellpadding="6" 
               style="border-collapse: collapse; font-family: Arial; font-size: 14px;">
            <tr style="background-color: #f2f2f2; font-weight: bold;">
        """

        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>"

        for row in results:
            html += "<tr>"
            for col in row:
                html += f"<td>{col}</td>"
            html += "</tr>"

        html += "</table>"

    # Push formatted HTML for next task
    ti.xcom_push(key='formatted_html', value=html)
