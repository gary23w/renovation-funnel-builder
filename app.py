import json
import os
import shutil
from datetime import datetime
import cssutils
import csscompressor
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TemplateLoader:
    def __init__(self, template_path, config_path):
        self.template = self._load_file(template_path)
        self.config = self._load_json(config_path)
        self.inline_css = ""

    @staticmethod
    def _load_file(path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except IOError as e:
            logging.error(f"Error reading file {path}: {e}")
            return None

    @staticmethod
    def _load_json(path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except IOError as e:
            logging.error(f"Error reading json file {path}: {e}")
            return None

    def replace_placeholder(self, placeholder, content):
        if content.startswith('images/'):
            img_to_webp = content.split('.')[0] + '.webp'
            self.template = self.template.replace(f"{{{{ {placeholder} }}}}", img_to_webp)
        else:
            self.template = self.template.replace(f"{{{{ {placeholder} }}}}", content)

    def render_template(self):
        self.replace_placeholder("inlineCss", f"<style>{self.inline_css}</style>")
        for item in self.config:
            for key, value in item.items():
                content = self.get_content_loader(key).load_content(value) if isinstance(value, list) else value
                self.replace_placeholder(key, content)
        self._save_rendered_template()

    def render_styles_and_minify(self):
        css_path = 'src/css/gary.css'
        theme_color = self.config[0].get('websiteThemeColor')
        button_color = self.config[0].get('websiteButtonColor')
        button_border = self.config[0].get('websiteButtonBorderColor')
        li_start_color = self.config[0].get('websiteLiStartColor')
        li_end_color = self.config[0].get('websiteLiEndColor')
        css_text = self._customize_css(css_path, theme_color, button_color, button_border, li_start_color, li_end_color)
        self.inline_css = csscompressor.compress(css_text)

    def _customize_css(self, css_path, theme_color, button_color, button_border, li_start_color, li_end_color):
        css_text = self._load_file(css_path)
        sheet = cssutils.parseString(css_text)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    if 'primary-color' in property.name:
                        property.value = theme_color
                    if 'button-color' in property.name:
                        property.value = button_color
                    if 'button-border' in property.name:
                        property.value = button_border
                    if 'li-background-start' in property.name:
                        property.value = li_start_color
                    if 'li-background-end' in property.name:
                        property.value = li_end_color
                    
        prod_css_dir = 'prod/src/css'
        os.makedirs(prod_css_dir, exist_ok=True)
        with open(f'{prod_css_dir}/gary.css', 'w') as file:
            file.write(sheet.cssText.decode('utf-8'))
        shutil.copy('src/css/garydation.css', f'{prod_css_dir}/garydation.css')
        return sheet.cssText.decode('utf-8')

    def get_content_loader(self, key):
        loader_map = {
            "serviceMainList": ServiceMainListLoader(),
            "detailedServiceList": DetailedServiceListLoader(),
            "surveySteps": SurveyStepsLoader(),
            "galleryImages": GalleryImagesLoader(),
            "reviews": ReviewsLoader(),
        }
        return loader_map.get(key, DefaultLoader())

    def _save_rendered_template(self):
        with open("prod/index.html", "w") as file:
            file.write(self.template)

    def convert_images_to_webp(self, image_directory):
        for subdir, dirs, files in os.walk(image_directory):
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            for file in image_files:
                filepath = os.path.join(subdir, file)
                self._convert_image(filepath)

    @staticmethod
    def _convert_image(image_path):
        im = Image.open(image_path)
        base = os.path.splitext(image_path)[0]
        im.save(f"{base}.webp", "WEBP")

    def build_web_manifest(self):
        manifest_details = self.config[0].get("manifest_details", [{}])[0]
        with open("prod/manifest.json", "w") as manifest_file:
            json.dump(manifest_details, manifest_file, indent=2)

    def generate_sitemap(self):
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
        main_url = self.config[0].get('websiteEndpoint', '')  
        datetime_xml = datetime.now().strftime("%Y-%m-%d")
        if main_url:
            sitemap_content += f"""
        <url>
        <loc>{main_url}</loc>
        <lastmod>{datetime_xml}</lastmod>  # Assuming you have a lastModified key; adjust as necessary
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
        </url>"""

        sitemap_content += "</urlset>"

        with open("prod/sitemap.xml", "w") as sitemap_file:
            sitemap_file.write(sitemap_content)

class ContentLoader:
    def load_content(self, content):
        raise NotImplementedError("Subclasses must implement this method")

class ServiceMainListLoader(ContentLoader):
    def load_content(self, serviceMainList):
        serviceList = ""
        for service in serviceMainList:
            tplObject = """
                <div class="cell small-12 medium-6 large-3">
                  <div class="service-item">
                    <img class="lazy-load" src="{img}" data-src="{img}" alt="{title}" />
                    <h3>{title}</h3>
                    <p>{description}</p>
                  </div>
                </div>
            """
            tplObject = tplObject.format(**service)
            serviceList += tplObject
        return serviceList

class DetailedServiceListLoader(ContentLoader):
    def load_content(self, detailedServiceList):
        serviceList = "".join(["<li>" + str(service) + "</li>" for service in detailedServiceList])
        return serviceList

class SurveyStepsLoader(ContentLoader):
    def load_content(self, surveySteps):
        surveyList = ""
        for step in surveySteps:
            tplObject = """
            <div class="step">
              <div class="step-number">{title}</div>
              <p class="step-description">
                <strong>{description}</strong>
              </p>
            </div>
            """
            tplObject = tplObject.format(**step)
            surveyList += tplObject
        return surveyList

class GalleryImagesLoader(ContentLoader):
    def load_content(self, galleryImages):
        galleryList = ""
        for image in galleryImages:
            img_to_webp = image['img'].split('.')[0] + '.webp'
            tplObject = """
            <div class="gallery-item">
                <img class="lazy-load" src="{img_to_webp}" data-src="{img_to_webp}" alt="{alt}" />
            </div>
            """
            tplObject = tplObject.format(img_to_webp=img_to_webp, **image)
            galleryList += tplObject
        return galleryList

class ReviewsLoader(ContentLoader):
    def load_content(self, reviews):
        reviewList = ""
        for review in reviews:
            tplObject = """
            <div class="cell small-12 medium-6 large-4">
                  <div class="review-item callout">
                    <div class="grid-container">
                        <div class="grid-x grid-margin-x align-top">
                            <div class="cell small-12">
                                <div class="rating-box">
                                    <p class="review-stars">{stars}</p>
                                    <p class="review-rating">Rated {rating}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                        <p class="review-text">
                        "{description}"
                        </p>
                        <p class="review-author">- {name}</p>
                    </div>
                </div>
                """
            tplObject = tplObject.format(**review)
            reviewList += tplObject
        return reviewList

class DefaultLoader(ContentLoader):
    def load_content(self, content):
        return str(content)

def empty_prod():
    if os.path.exists('prod/'):
        for filename in os.listdir('prod/'):
            file_path = os.path.join('prod/', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs('prod/')

def copy_directory(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok=True)

def copy_files_from_directory(src, dest):
    for item in os.listdir(src):
        src_item_path = os.path.join(src, item)
        dest_item_path = os.path.join(dest, item)
        if os.path.isfile(src_item_path):
            shutil.copy2(src_item_path, dest_item_path)

if __name__ == "__main__":
    empty_prod()

    template_loader = TemplateLoader('tpl/template.html', 'configs/example.json')

    if input("Do you want to convert images to WebP format? (y/n): ").lower() == 'y':
        logging.info("[*] Converting images to WebP format")
        template_loader.convert_images_to_webp('images')
        template_loader.convert_images_to_webp('images/stock')

    logging.info("[*] Customizing and minifying CSS")

    template_loader.render_styles_and_minify()

    logging.info("[*] Rendering template")

    template_loader.render_template()

    logging.info("[*] Building web manifest")

    template_loader.build_web_manifest()

    logging.info("[*] Generating sitemap")

    template_loader.generate_sitemap()

    logging.info("[*] Building dir structure for prod/")

    copy_directory('src/scripts', 'prod/src/scripts')

    copy_files_from_directory('utils', 'prod')

    copy_directory('images', 'prod/images')

    copy_directory('videos', 'prod/videos')

    logging.info("[*] Site build complete, and directories copied to prod/")
