
$.fn.outerFind=function(a){return this.find(a).addBack(a)};
function initTabs(a){0!==$(a).find(".nav-tabs").length&&$(a).outerFind('section[id^="tabs"]').each(function(){var a=$(this).attr("id"),b=$(this).find(".nav-tabs .nav-item"),c=$(this).find(".tab-pane");c.removeClass("active").eq(0).addClass("active");b.find("a").removeClass("active").removeAttr("aria-expanded").eq(0).addClass("active");c.each(function(){$(this).attr("id",a+"_tab"+$(this).index())});b.each(function(){$(this).find("a").attr("href","#"+a+"_tab"+$(this).index())})})}var isBuilder=$("html").hasClass("is-builder");
if(isBuilder)$(document).on("add.cards",function(a){initTabs(a.target)});else"undefined"===typeof window.initTabsPlugin&&(window.initTabsPlugin=!0,console.log("init tabs by plugin"),initTabs(document.body));
