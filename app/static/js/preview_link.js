
      const linkPreviewGenerator = require("link-preview-generator");


        async function start() {
                    const previewData = await linkPreviewGenerator(
                      "https://www.youtube.com/watch?v=8mqqY2Ji7_g"
                    );
                    return  previewData; 
                  }

                start().then(result => {
                console.log(result);
          })