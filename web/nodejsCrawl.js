const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const naver_id = "삼성";
  String.prototype.replaceAll = function(org, dest) {
    return this.split(org).join(dest);
}
    
//   const naver_pw = "네이버 비밀번호";
  await page.goto('http://surffing.net/');
  await page.evaluate((id) => {
    document.querySelector('#saerchKeyword').value = id;
    // document.querySelector('#pw').value = pw;
  }, naver_id);


    // const navigationPromise = page.waitForNavigation({ waitUntil:'domcontentloaded', timeout: 1002 });
    // page.click('.key-btn');
    // await navigationPromise;
    await page.click('.key-btn');

    await page.waitFor(2000);
    const element1= await page.evaluate(()=>{
      const anchors= Array.from(document.querySelectorAll('td.center'));
      return anchors.map(anchor => anchor.textContent);
    });
    for(var i =0;i<element1.length;i++)
    {
      element1[i] = element1[i].replaceAll('\t','').replaceAll('\n','');
    }
    console.log(element1);
    


  //   const element1 = await page.$('td');
  //   element1 = await page.evaluate(element1=>element1.value,element1);
  //   console.log(element1);
  // //   await page.evaluate(() => {
  // //   console.log(document.querySelector('td'));
  // //   // console.log(document.querySelector('//td').value);
  // // });
  console.log("superpower");
  
  await page.screenshot({ path: 'surffing.png', fullPage:true });
  await browser.close();
})();