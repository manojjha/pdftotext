from django.shortcuts import render
from django.http import HttpResponse

import io,os
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.shortcuts import render

from google.cloud import vision
from google.cloud.vision import types

from PIL import Image, ImageDraw
from converter.models import history

from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'index.html')


def info(request):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'kal-kal-1532846232334-738abd5f7e5a.json'
    image_context = types.ImageContext(language_hints =["iw"])
    client = vision.ImageAnnotatorClient()

    myfile = request.FILES["pic"]
    print("myfile name data>>>>>>>>>>>>>>>>>>>>>>>>>",myfile)
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    file_name = fs.url(filename)
    #image_file= r'C:\Users\mjha3\Desktop\Django_project\VisionAPI_Test\PDFtoTEXT\pdftotext\pdftotext\media\2020_07_30 00_23 Office Lens (3)3.jpg'
    print("Image file location>>>>>>>",image_file)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    response = client.document_text_detection(image=image,image_context=image_context)
    document = response.full_text_annotation

    bounds = []
    doctext = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                #print(u'Paragraph Confidence: {}\n'.format(paragraph.confidence))

                block_text = ''
                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)
                    word_text = ''
                    for symbol in word.symbols:
                        word_text = word_text + symbol.text
                        #print(u'\tSymbol text: {} (confidence: {})'.format(symbol.text, symbol.confidence))

                    #print(u'Word text: {} (confidence: {})\n'.format(word_text, word.confidence))

                    block_text += ' ' + word_text

                #print(u'Block Content: {}\n'.format(block_text))
                #print(u'Block Confidence:\n {}\n'.format(block.confidence))
                bounds.append(block.bounding_box)
                doctext.append(block_text + "\n")
                print("data value of doctext >>>>>>>>>>>>>>>..",doctext.append(block_text + "\n"))

    #return (bounds,doctext)
    return render(request, 'results.html', {"labels":doctext, 'image': image_file})

def getHistory(request):
    previous_searches = history.objects.all()
    return render(request, 'history.html', {"data":previous_searches})







    '''vision_client = vision.ImageAnnotatorClient()
    myfile = request.FILES["pic"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    file_name = fs.url(filename)
    with io.open(file_name, "rb") as image_file:
        content = image_file.read()
        image = types.Image(content=content)
    labels = image.detect_labels()
    label_data = ""
    for label in labels:
        label_data= label_data+label.description+"="+str(label.score)+","
    record = history(url=file_name, data= label_data)
    record.save()'''