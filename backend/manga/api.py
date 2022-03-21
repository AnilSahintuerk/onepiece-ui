
from flask import Flask
from flask_restful import Resource, Api
from extensions import OPManga
from opmangabot import manga_email


app = Flask(__name__)
api = Api(app)

class Chapter(Resource):
    def get(self, email, chapter_id):
        OPManga.OPMake().make_chapter(chapter_id)
        manga_email.main(email, chapter_id)
        return {'email': email, 'chapter': chapter_id}

api.add_resource(Chapter, '/<string:email>/<string:chapter_id>')

if __name__ == '__main__':
    app.run(debug=True)