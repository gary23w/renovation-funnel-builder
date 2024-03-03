# Funnel Overview

This project originated from the idea of creating an effective marketing funnel by leveraging a proven template. During my preliminary research, I observed that most high-converting funnels were proprietary, requiring a purchase. However, equipped with time and patience, I derived a working concept inspired by a funnel I saw on a YouTube video. This initial exploration led me to adopt the Foundation library as the cornerstone of my development strategy. The outcome was a rapidly assembled working prototype, closely modeled on the visuals/screenshots provided from the youtube video. While further research might have unearthed a similar template, the chosen path provided invaluable hands-on experience.

## Features and Innovations

#### Dynamic Configuration Loader

One of the key innovations of this project is the implementation of a dynamic loading feature(config files). This functionality facilitates the construction of configurations using AI, enabling the generation of funnels on-the-fly. It's crucial to maintain strict configurations to ensure the HTML and page designs remain intact and functional.

## Image Configuration Challenges

Configuring images posed a significant challenge, primarily due to licensing constraints. To address this, version 0.1 mandates users to supply their own images pertinent to the funnel, ensuring compliance and authenticity.

## Legal Compliance and Privacy

An essential component of deploying a funnel involves legal and privacy considerations. I've crafted a comprehensive privacy policy that adheres to European laws, data protection standards, and educational purposes. Additionally, a disclaimer mitigates legal liabilities associated with the webpage.

## Random Thoughts

The project now embarks on automating funnel processes for four main renovation services, emphasizing the creation of static, secure, and reliable pages. The initial step involves populating a configuration file, found in the configs directory, which can be facilitated by a Large Language Model (LLM) for efficiency. Selecting an appropriate theme and style is crucial, as it reflects the brand identity. This static funnel is meticulously optimized for performance, accessibility, best practices, and SEO, achieving top scores across these categories.

## Technical Implementation

#### Image Processing

The build process includes a script to convert and compress images (PNG, JPG, JPEG) into the WebP format, significantly enhancing loading times. Users are encouraged to approve this feature upon execution.

## CSS Integration

The project incorporates an innovative approach to CSS management by inlining the src/css/gary.css sheet directly into the markdown, circumventing certain bugs by deferring the CSS loading into the page.

### Deployment and Hosting

The static site generated is located within the prod/ directory, ready for deployment. For those interested in containerization, a start.sh script is provided to facilitate deployment to Docker, utilizing Apache for hosting and .htaccess to ensure browser security.
