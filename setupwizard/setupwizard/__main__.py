from sanic import Sanic, response

app = Sanic(name="setupwizard")


@app.route("/")
async def test(request):
    return response.html(
        '''\
<div style="background: red;">hello setupwizard</div>
<div>
    <a href="/go-main">Launch Main App</a>
</div>
'''
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
