const CLASSNAME = "-visible";
const TIMEOUT = 500;
const $target = $(".title");

const intervalId = setInterval(() => {
  $target.addClass(CLASSNAME);
  }, TIMEOUT);
