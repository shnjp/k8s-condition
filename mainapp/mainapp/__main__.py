from sanic import Sanic, response

app = Sanic(name="mainapp")


@app.route("/")
async def test(request):
    return response.html(
        '''\
<div style="background: red;">hello MAIN</div>
'''
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
