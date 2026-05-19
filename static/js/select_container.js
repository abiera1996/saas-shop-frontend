
class SelectionContainer {
    constructor(container, overlay, btnClass, listInput) {
        this.container = container;
        this.overlay = overlay;
        this.btnClass = btnClass;
        this.marks = [];
        this.listInput = listInput;
    }

    overlayClicked(event){
        let x = event.offsetX;
        let y = event.offsetY;
        let color = this.getCurrentColor();

        if (color === "transparent") {
            let markToRemove = this.findMarkAtPosition(x, y);
            if (markToRemove) {
                markToRemove.element.parentNode.removeChild(markToRemove.element);
                this.marks = this.marks.filter(function(mark) {
                    return mark.element !== markToRemove.element;
                });
            }
        } else {
            let mark = document.createElement("div");
            mark.className = "selected-mark mark-" + color;
            mark.style.left = (x - 3) + "px"; // Adjust position to center the mark
            mark.style.top = (y - 3) + "px"; // Adjust position to center the mark

            if (color !== null){
                document.getElementById(this.container).appendChild(mark);
                this.marks.push({ color: color, x: x, y: y, element: mark });
            }
        }
        document.getElementById(this.listInput).value = JSON.stringify(this.marks)
        // console.log(document.getElementById(this.listInput).value.toString())
        // console.log(this.marks)
    }

    getCurrentColor(){
        let buttons = document.getElementsByClassName(this.btnClass);
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i].classList.contains("active")) {
                return buttons[i].getAttribute('data-color');
            }
        }
        return null;
    }

    findMarkAtPosition(x, y) {
        for (let i = this.marks.length - 1; i >= 0; i--) {
            let mark = this.marks[i];
            let rect = this.getMarkRect(mark);
            if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
                return mark;
            }
        }
        return null;
    }

    getMarkRect(mark) {
        let size = 10; // half of the mark's width/height
        return {
            left: mark.x - size,
            right: mark.x + size,
            top: mark.y - size,
            bottom: mark.y + size
        };
    }

    getMarkings() {
        return this.marks
    }
}

const myObject = new SelectionContainer();