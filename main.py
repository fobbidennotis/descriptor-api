import asyncio
from image_describer import Img
from models import READER_RU, READER_EN, MODEL, PROCESSOR
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/describe/", methods=["POST"])
async def describe_handler():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    image_bytes = file.read()

    return jsonify(
        {
            "description": await Img(
                PROCESSOR, MODEL, READER_EN, READER_RU, image_bytes
            ).describe_image()
        }
    ), 200


async def main() -> None:
    app.run()


if __name__ == "__main__":
    asyncio.run(main())
