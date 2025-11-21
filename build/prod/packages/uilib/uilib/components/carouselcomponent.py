from uilib.basecomponents import Component
from uilib.renderresponse import RenderResponse
import json


class CarouselComponent(Component):

    def __init__(self, title=None, description=None, images=[]):
        self.title = title
        self.description = description
        self.images = images


    def render(self):

        html = f'''
<div style="width: 90%; margin: 0 auto;">
    {f'<h2 class="text-center">{self.title}</h2>' if self.title else ''}
    {f'<p class="text-center">{self.description}</p>' if self.description else ''}
    <div class="carousel-container" style="background-color: #E0E0E0;">
        <div class="row align-items-center">
            <div class="col-1 text-center">
                <i class="bi bi-arrow-left-circle carousel-prev" style="font-size: 2rem; padding-left: 20px; cursor: pointer;"></i>
            </div>
            <div class="col-10">
                <img id="carousel-image" src="{self.images[0]['url'] if self.images else ''}" 
                     style="width: 100%; display: block; margin: 0 auto; padding-top: 20px; padding-bottom: 20px; transition: opacity 0.3s ease;">
            </div>
            <div class="col-1 text-center">
                <i class="bi bi-arrow-right-circle carousel-next" style="font-size: 2rem; padding-right: 20px; cursor: pointer;"></i>
            </div>
        </div>
    </div>
</div>
'''
        
        js = '''
<script>
document.addEventListener('DOMContentLoaded', function() {
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    const carouselImg = document.getElementById('carousel-image');
    const carouselLegend = document.getElementById('carousel-legend');
    const carouselImages = ''' + json.dumps(self.images) + ''';
    let currentImageIndex = 0;
    
    // Preload all images
    carouselImages.forEach(image => {
        const img = new Image();
        img.src = image.url;
    });

    function updateImage(direction) {
        if (direction === 'next') {
            currentImageIndex = (currentImageIndex + 1) % carouselImages.length;
        } else {
            currentImageIndex = (currentImageIndex - 1 + carouselImages.length) % carouselImages.length;
        }
        
        carouselImg.src = carouselImages[currentImageIndex].url;
        carouselLegend.textContent = carouselImages[currentImageIndex].legend;
    }

    prevBtn.addEventListener('click', () => updateImage('prev'));
    nextBtn.addEventListener('click', () => updateImage('next'));
});
</script>
'''



        return RenderResponse(html=html, footer_js=js)

    @staticmethod
    def example():
        comp = CarouselComponent(
            title="Example Carousel",
            description="Example Carousel Description",
            images=[
                {
                    "url": "https://via.placeholder.com/800x400?text=Example+1",
                    "legend": "Example image 1 description"
                },
                {
                    "url": "https://via.placeholder.com/800x400?text=Example+2",
                    "legend": "Example image 2 description"
                },
                {
                    "url": "https://via.placeholder.com/800x400?text=Example+3",
                    "legend": "Example image 3 description"
                }
            ]
        )
        return comp


#         html = f'''
# <div style="width: 90%; margin: 0 auto;">
#     {f'<h2 class="text-center">{self.title}</h2>' if self.title else ''}
#     {f'<p class="text-center">{self.description}</p>' if self.description else ''}
#     <div class="carousel-container" style="background-color: #E0E0E0;">
#         <div class="row align-items-center">
#             <div class="col-1 text-center">
#                 <i class="bi bi-arrow-left-circle" style="font-size: 2rem; padding-left: 20px;"></i>
#             </div>
#             <div class="col-10">
#                 <img src="/statics/ss_home.png" style="width: 100%; display: block; margin: 0 auto; padding-top: 20px; padding-bottom: 20px;">
#             </div>
#             <div class="col-1 text-center">
#                 <i class="bi bi-arrow-right-circle" style="font-size: 2rem; padding-right: 20px;"></i>
#             </div>
#         </div>
#     </div>
# </div>
#     '''