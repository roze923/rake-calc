from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """<!doctype html>
<title>還元率計算ツール</title>
<h2>還元率自動計算</h2>
<form method='POST'>
  エントリー費（円）: <input name='entry_fee' type='number'><br>
  エントリー数: <input name='entry_count' type='number'><br>
  賞金総額（円）: <input name='total_prize' type='number'><br>
  チケット枚数: <input name='ticket_count' type='number'><br>
  1チケットの価値（円）: <input name='ticket_value' type='number' value='20000'><br>
  <input type='submit' value='計算'>
</form>
{% if result %}
<hr>
<p>総参加費: {{ result.total_cost }} 円</p>
<p>賞金総額（円）: {{ result.prize_total }} 円</p>
<p><strong>還元率: {{ result.rakeback }} %</strong></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        entry_fee = int(request.form["entry_fee"])
        entry_count = int(request.form["entry_count"])
        total_cost = entry_fee * entry_count

        if request.form["total_prize"]:
            prize_total = int(request.form["total_prize"])
        else:
            ticket_count = int(request.form["ticket_count"])
            ticket_value = int(request.form["ticket_value"])
            prize_total = ticket_count * ticket_value

        rakeback = round((prize_total / total_cost) * 100, 2)
        result = {"total_cost": total_cost, "prize_total": prize_total, "rakeback": rakeback}

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)
