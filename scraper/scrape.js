const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const url = process.env.SCRAPE_URL;

console.log(`Scraping started: ${url}`);

if (!url) {
  console.error("Please provide SCRAPE_URL environment variable.");
  console.error("Example: SCRAPE_URL=https://example.com");
  console.error("Usage: docker run -p 5000:5000 -e SCRAPE_URL='https://example.com' <IMAGE_NAME>");
  process.exit(1);
}

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
      executablePath: '/usr/bin/chromium'
    });

    const page = await browser.newPage();
    
    console.log("Scraping in progress...");
    
    const response = await page.goto(url, { 
      waitUntil: 'networkidle2',
      timeout: 30000
    });
    
    if (!response.ok()) {
      console.warn(`HTTP response status: ${response.status()}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const data = await page.evaluate(() => {
      const title = document.title;
      const heading = document.querySelector('h1')?.innerText || 
                     document.querySelector('h2')?.innerText || 'No heading found';
      
      const metaDescription = document.querySelector('meta[name="description"]')?.getAttribute('content') || 
                             document.querySelector('meta[property="og:description"]')?.getAttribute('content') || 
                             'No meta description';
      
      const firstParagraph = document.querySelector('p')?.innerText || 'No paragraph found';
      
      const links = Array.from(document.querySelectorAll('a'))
        .map(link => ({
          text: link.innerText.trim() || link.getAttribute('aria-label') || 'No text',
          href: link.href
        }))
        .filter(link => link.href.startsWith('http') && link.text);

      return {
        title,
        metaDescription,
        firstParagraph,
        heading,
        totalLinks: links.length,
        links: links.slice(0, 10)
      };
    });

    await browser.close();
    
    // Save the complete data to the JSON file
    const outputPath = path.resolve(process.cwd(), 'scraped_data.json');
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
    
    // Also save the data with markers for the Python app to a separate file
    const parsedOutputPath = path.resolve(process.cwd(), 'parsed_data.txt');
    fs.writeFileSync(parsedOutputPath, `JSON_START\n${JSON.stringify(data)}\nJSON_END`);
    
    console.log(`Scraping completed successfully!`);
    console.log(`You can access the data at http://127.0.0.1:5000`);
    
  } catch (error) {
    console.error(`Error during scraping: ${error.message}`);
    process.exit(1);
  }
})();
