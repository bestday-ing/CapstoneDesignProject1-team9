// nodejs 크롤링을 위한 모듈
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  //키워드값 넣는곳
  const keyword = "치킨";
  //해당 사이트로 간다
  await page.goto('http://surffing.net/');
  //입력상자에 값넣기
  await page.evaluate((id) => {
    document.querySelector('#saerchKeyword').value = id;
    // document.querySelector('#pw').value = pw;
  }, keyword);
  //검색버튼 클릭
    await page.click('.key-btn');
    //약 2초 동안 대기함, 시간줄이면 잘 안됨
    await page.waitFor(2000);
    //밑에 페이지 변동됐을때 해당리스트에서 값 뽑아옴
    const element1= await page.evaluate(()=>{
      const anchors= Array.from(document.querySelectorAll('td'));
      return anchors.map(anchor => anchor.textContent); //각 원소마다 textContent, 즉 문자값을 받아옴
    });
    //값에 \t와 \n이 들어가있는 경우가 있어서 그것을 대체해주는 함수
    String.prototype.replaceAll = function(org, dest) {
      return this.split(org).join(dest);
  }
  //원소별로 replaceall 해줌
    for(var i =0;i<element1.length;i++)
    {
      element1[i] = element1[i].replaceAll('\t','').replaceAll('\n','');
    }
    // 원소 배열들에게 나누기
    relatedKeywords = {}  //연관 검색어 : [pc, mobile]
    publishVolumes = {}  // blog : 발행량, cafe : 발행량, knwlgin : 발행량
    var count=0;
    for(var i=0;i<3;i++)
    {
      count +=1;
      if(count % 3 ==1) //월간 블로그 발행량
        publishVolumes['blog'] = element1[i];
      else if(count %3 ==2)//월간 카페 발행량
        publishVolumes['cafe']= element1[i];
      else//월간지식인 발행량
        publishVolumes['knwlgin']= element1[i];
    }
    // 연관검색어들의 정보를 담을 애들
    var bufferKey = "";
    var bufferPC = "";
    var bufferM = "";
    count = 0;
    for(i=6;i<element1.length;i++){
    count += 1

    if(count % 3 == 1)  // 연관 검색어
        bufferKey = element1[i]
    else if(count % 3 == 2)  // 월간 검색수 PC
        bufferPC = element1[i]
    else  //월간 검색수 모바일
        bufferM = element1[i]

    relatedKeywords[bufferKey] = [bufferPC, bufferM]
    }
    console.log(publishVolumes);
    console.log(relatedKeywords);

  //screenshot찍어서 나옴, 테스트용, 지워도됨
  await page.screenshot({ path: 'surffing.png', fullPage:true });
  //browser 종료, 지우면 안됨
  await browser.close();
})();