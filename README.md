# Funnel Project Overview

The Funnel project aims to democratize access to high-converting marketing funnels without the need to purchase proprietary templates. Drawing inspiration from a funnel showcased in a YouTube video, this project adopts the Foundation library to rapidly prototype a visually appealing and functional marketing funnel.

## Key Features and Innovations

### Dynamic Configuration Loader

- A standout feature is the dynamic configuration loader, which allows for on-the-fly funnel generation with AI-powered configuration setups. This ensures the HTML and page designs are both intact and functional.

### Challenges in Image Configuration

- Due to licensing constraints, users are required to provide their own images for the funnel in version 0.1, ensuring both compliance and authenticity.

### Legal Compliance and Privacy

- The project includes a comprehensive privacy policy compliant with European standards and a disclaimer to mitigate legal liabilities, prioritizing data protection and educational use.

## Project Insights

The next phase focuses on automating funnel processes for renovation services, creating static yet dynamic, secure, and SEO-optimized pages. The process begins with populating a configuration file via a Large Language Model (LLM) for enhanced efficiency and selecting themes that best represent the brand identity.

## Technical Details

### Image Processing

- The build process involves a script for converting images to WebP format, significantly improving site loading times.

### CSS Integration

- CSS management is streamlined by inlining the `src/css/gary.css` directly into the markup, solving certain bugs by deferring CSS loading.

## Deployment and Hosting

The project results in a static site located within the `prod/` directory, poised for deployment. For containerization:

- **Build Methods**:
  - Execute `python3 app.py` for initial build processes.
  - Navigate to the `prod/` directory post-build. Here, you can deploy a Docker container containing the funnel system by executing either `build.sh` for Unix/Linux systems or `build.ps1` for Windows users.

### Containerization with Docker

- A `start.sh` script (for Unix/Linux) or `build.ps1` script (for Windows) is available for deploying the static site to Docker, leveraging Apache for hosting and utilizing `.htaccess` for enhanced browser security.

After completing the build process, users can deploy their funnel with ease, ensuring a secure, efficient, and legally compliant web presence.

#### Notes:

Really just wanted to automate the whole sales funnel deployment here. My intent, knowing that compliance was an issue. Is to have a system that interfaces with a model to generate configs(server rendering documents) on the fly. From here, our build process will take over and complete the "funnel" package, plus prep it for deployment.
Simplicity of this was key, as the entire "sales funnel" eco system is bloated with proprietary hoggendaus.
Hoggendaus, no more. Everything from styles to unique configurations is steeped by the power of artificial intelligence!
