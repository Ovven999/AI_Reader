// loadBook(bookUrl: HTMLInputElement) {
//     this.bookUrl = bookUrl.value;
//     console.log(this.bookUrl)
//     this.http.get(this.bookLinkSource, { responseType: 'text' }).subscribe(
//       (data) => {
//         // Parse the data here
//         const lines = data.split('\n');
//         const chapters = lines.map(line => {
//           const [namePart, urlPart] = line.split(', ').map(part => part.split(': ')[1]);

//           // Find the first space and get the substring from the next character
//           const title = namePart?.substring(namePart.indexOf(' ') + 1).trim();
          
//           return { title, url: urlPart?.trim() };
//         }).filter(chapter => chapter.title && chapter.url);

//         this.chapterLinks = chapters;
//         console.log(this.chapterLinks); // Processed chapters

//         this.groupedChapterLinks = [];
//         for (let i = 0; i < this.chapterLinks.length; i += 3) {
//           this.groupedChapterLinks.push(this.chapterLinks.slice(i, i + 3));
//         }
//       }
//     );
//     return;
//   }