import Konva from 'konva';
import { RobotModel } from './robot_model';
import $ from 'jquery';
import _isNumber from 'lodash/isNumber';
import _random from 'lodash/random';
import _padStart from 'lodash/padStart';

const walls_config: { [key: string]: any } = {
  normal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 10,
  },

  removable: {
    x: 50,
    y: 25,
    stroke: '#de1738',
    strokeWidth: 10,
  },

  goal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 7,
    dash: [5, 5],
  },
};

let MAX_WIDTH = 600;
let MAX_HEIGHT = 600;
let MAX_ROWS = 20;
let MAX_COLS = 20;
let LEFT_PADDING = 50;
let MARGIN_NUMBER_CIRCLE = 2;
export class WorldModel {
  rows: number;
  cols: number;
  vwalls: any;
  hwalls: any;
  robots: any;
  width: number;
  height: number;
  bs: number;
  objects: any;
  tileMap: any;
  tiles: any;
  messages: any;
  pending_goals: any;
  drop_goals: any;
  flags: any;
  stats: {
    basket?: any;
    current_load?: number;
    max_capacity?: null | number;
    total_moves?: number;
  };
  ui: {
    wrapper: HTMLDivElement;
    stage?: Konva.Stage;
    stageHeight: number;
    stageWidth: number;
    layers: {
      main: Konva.Layer;
      line: Konva.Layer;
      msg?: Konva.Layer;
      bg: Konva.Layer;
    };
  };

  constructor() {
    this.init_ui();
  }

  init(
    rows: number,
    cols: number,
    vwalls = [],
    hwalls = [],
    robots = [],
    objects = {},
    tileMap = {},
    tiles = [],
    messages = {},
    flags = {},
    pending_goals = [],
    drop_goals = []
  ) {
    this.rows = Math.min(MAX_ROWS, rows);
    this.cols = Math.min(MAX_COLS, cols);
    this.vwalls = vwalls;
    this.hwalls = hwalls;
    this.bs = Math.ceil(
      Math.min(MAX_HEIGHT / this.rows, MAX_WIDTH / this.cols, 50)
    );

    this.height = rows * this.bs;
    this.width = cols * this.bs;
    this.objects = objects;
    this.tileMap = tileMap;
    this.tiles = tiles;
    this.pending_goals = pending_goals;
    this.drop_goals = drop_goals;
    this.messages = messages;
    this.flags = flags;
    this.draw_canvas();

    this.robots = robots.map(
      (robot: RobotModel, i: number) =>
        new RobotModel(
          i,
          this,
          robot.x,
          robot.y,
          robot.orientation,
          robot.image
        )
    );

    console.log(robots);

    this.robots[0].draw();
  }

  init_ui() {
    let wrapper = document.createElement('div');
    wrapper.setAttribute('class', 'ttgt-wrapper');
    let elem = document.createElement('div');
    elem.setAttribute('id', 'container');

    let bttnTxt = document.createElement('span');
    let txtNode = document.createTextNode('Toggle');
    bttnTxt.appendChild(txtNode);
    bttnTxt.setAttribute('class', 'bttn-txt');

    let sidebar = document.createElement('button');
    sidebar.appendChild(bttnTxt);
    sidebar.setAttribute('class', 'ttgt-sidebar-bttn');
    sidebar.onclick = function () {
      $('#container').toggle();
    };

    wrapper.appendChild(elem);
    wrapper.appendChild(sidebar);

    this.ui = {
      wrapper,
      stageHeight: this.height + this.bs,
      stageWidth: Math.max(this.width, 500) + this.bs,
      layers: {
        bg: new Konva.Layer({ offsetY: -150 }),
        main: new Konva.Layer({ offsetY: -150 }),
        line: new Konva.Layer({ offsetY: -150 }),
      },
    };
  }

  draw_canvas() {
    let padding = 25;
    let msgHeight = 150;
    this.ui.stageHeight = this.height + this.bs + padding + msgHeight;
    this.ui.stageWidth = Math.max(this.width, 500) + this.bs + padding;
    let stage = new Konva.Stage({
      container: 'container',
      width: this.ui.stageWidth,
      height: this.ui.stageHeight,
    });

    this.ui.layers.msg = new Konva.Layer({
      width: 500 + this.bs + padding,
      height: msgHeight,
    });

    stage.add(this.ui.layers.msg);
    stage.add(this.ui.layers.bg);
    stage.add(this.ui.layers.main);
    stage.add(this.ui.layers.line);
    this.ui.stage = stage;

    //draw stage
    this.draw_border();
    this.draw_grid();
    this.draw_objects();
    this.draw_stats();
    this.draw_msg_containers();
    this.draw_envelops();
    this.draw_flags();

    this.draw_drop_goals(this.drop_goals);

    if (this.pending_goals.length > 0) {
      this.draw_pending_instructions(this.pending_goals, 'red');
    } else {
      this.draw_pending_instructions(this.pending_goals);
    }

    this.ui.layers.main.draw();
  }

  draw_msg_containers() {
    let title = new Konva.Text({
      y: 60,
      width: 550,
      align: 'center',
      verticalAlign: 'center',
      height: 15,
      fontSize: 20,
      text: 'Pending Tasks',
    });

    this.ui.layers.msg?.add(title);
    this.ui.layers.msg?.draw();
  }

  draw_updated_stats() {
    let table = this.ui.layers.msg?.find(`.stats_table`)[0];
    if (table) {
      [
        this.stats.total_moves,
        this.stats.current_load,
        this.stats.max_capacity || 'Unlimited',
      ].map((msg, i) => {
        let k_txt = this.ui.layers.msg?.find(`.stats-table-val-${i}`)[0];
        if (k_txt) {
          //@ts-ignore
          k_txt.text(`${msg}`);
        }
      });
    }
    this.ui.layers.msg?.draw();
  }

  draw_stats() {
    let msg_layer = this.ui.layers.msg;
    let group = new Konva.Group({
      x: 40,
      y: 5,
    });

    let table = new Konva.Rect({
      width: 500,
      height: 40,
      stroke: 'gray',
      strokeWidth: 1,
      name: 'stats_table',
    });

    group.add(table);
    for (let i = 1; i < 3; i++) {
      let x1 = table.x() + Math.abs(table.width() / 3) * i;
      let y1 = table.y();
      let line = new Konva.Line({
        points: [x1, y1, x1, table.height()],
        strokeWidth: 1,
        stroke: 'gray',
      });
      group.add(line);
    }

    let hline = new Konva.Line({
      points: [
        table.x(),
        table.height() / 2,
        table.width() + table.x(),
        table.height() / 2,
      ],
      strokeWidth: 1,
      stroke: 'gray',
    });
    group.add(hline);
    let vals = [
      this.stats.total_moves,
      this.stats.current_load,
      this.stats.max_capacity || 'Unlimited',
    ];

    let cell_size = table.width() / 3.0;
    let x = table.x();

    ['TOTAL MOVES', 'CURRENT LOAD', 'MAX CAPACITY'].map((msg, i) => {
      let text = new Konva.Text({
        padding: 5,
        x: Math.abs(cell_size) * i + x,
        text: msg,
        strokeWidth: 5,
      });

      let val = new Konva.Text({
        padding: 5,
        x: Math.abs(cell_size) * i + x,
        y: Math.abs(table.height() / 2),
        text: `${vals[i]}`,
        strokeWidth: 10,
        fontSize: 16,
        name: `stats-table-val-${i}`,
      });

      group.add(text, val);
    });
    msg_layer?.add(group);
    msg_layer?.draw();
  }

  draw_pending_instructions(
    msgs = ['No Goal'],
    color = 'black',
    fontSize = 16
  ) {
    let msg_layer = this.ui.layers.msg;

    let old_msg = this.ui.layers.msg?.find(`.instruction_msg`)[0];

    if (old_msg) {
      old_msg.destroy();
    }

    let msg = msgs.slice(0, 3).join('\n');
    let rect_width = Math.max(msg_layer?.width() || 0, 200) - 70;
    let text = new Konva.Text({
      padding: 10,
      text: msg,
      x: 40,
      y: 90,
      align: 'left',
      fill: color,
      lineHeight: 1.2,
      fontSize: fontSize,
      width: rect_width,
      name: 'instruction_msg-rect',
    });

    let rect = new Konva.Rect({
      width: rect_width,
      height: text.height(),
      cornerRadius: 10,
      stroke: 'black',
      x: 40,
      y: 90,
      name: 'instruction_msg',
    });
    msg_layer?.add(rect);
    msg_layer?.add(text);
    msg_layer?.draw();
  }

  success_msg(msg: string | string[]) {
    let arr: string[] = [];

    let old_msg = this.ui.layers.msg?.find(`.instruction_msg`)[0];
    let old_msg_rect = this.ui.layers.msg?.find(`.instruction_msg-rect`)[0];

    if (old_msg) {
      old_msg.destroy();
      old_msg_rect?.destroy();
    }
    return this.draw_pending_instructions(arr.concat(msg), 'green', 20);
  }

  draw_objects() {
    for (const key in this.objects) {
      const [x, y] = key.split(',').map((zz) => parseInt(zz));
      this.draw_object(x, y, this.objects[key]);
    }
  }

  draw_flags() {
    for (const key in this.flags) {
      const [x, y] = key.split(',').map((zz) => parseInt(zz));
      this.draw_flag(x, y);
    }
  }

  draw_flag(x: number, y: number) {
    this.draw_custom('racing_flag_small', x, y, 0);
  }

  draw_object(x: number, y: number, obj: any) {
    for (const obj_name in obj) {
      let val = this.parse_value(obj[obj_name]);

      if (obj_name === 'beeper') {
        this.draw_beeper(x, y, val);
      } else {
        this.draw_custom(obj_name, x, y, val);
      }
    }
  }

  draw_envelops() {
    for (const key in this.messages) {
      const [x, y] = key.split(',').map((zz) => parseInt(zz));
      this.draw_envelop(x, y, this.messages[key]);
    }
  }

  draw_envelop(x: number, y: number, message: string) {
    this.draw_custom('envelope', x, y);
  }

  update_object(x: number, y: number, val: number) {
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    if (text) {
      //@ts-ignore
      text.text(`${val}`);
      this.ui.layers.main.draw();
    }
  }

  draw_beeper(x: number, y: number, val: number) {
    let radius = (0.6 * this.bs) / 2;
    let [cx, cy] = this.point2cxy(x + 1, y);
    cx = cx + radius * 2;
    let circle = new Konva.Circle({
      radius: radius,
      x: cx - 2.5,
      y: cy,
      fill: 'yellow',
      stroke: 'orange',
      strokeWidth: 5,
      name: `obj-${x}-${y}-circle`,
    });

    let num = new Konva.Text({
      text: `${val}`,
      x: cx - 7,
      y: cy - 7,
      fontSize: 18,

      name: `obj-${x}-${y}-text`,
    });

    this.ui.layers.main.add(circle, num);
  }

  remove_object(x: number, y: number) {
    let circle = this.ui.layers.main.find(`.obj-${x}-${y}-circle`)[0];
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    let img = this.ui.layers.main.find(`.obj-${x}-${y}-img`)[0];

    if (circle) {
      //@ts-ignore
      circle.destroy();
    }
    if (text) {
      //@ts-ignore
      text.destroy();
    }
    if (img) {
      //@ts-ignore
      img.destroy();
    }

    this.ui.layers.main.draw();
  }

  draw_sprite(sprite_name: string, x: number, y: number, frameRate = 1) {
    let spritePath = this.tileMap[sprite_name];
    let [cx, cy] = this.point2cxy(x, y);
    let sprite = new Image();
    sprite.src = spritePath;
    const animations = {
      motion: [0, 0, 40, 40, 40, 0, 40, 40],
    };
    let that = this;
    sprite.onload = function () {
      let imageSprite = new Konva.Sprite({
        x: cx + LEFT_PADDING,
        y: cy - that.bs / 2,
        name: `sprite-${x}-${y}-img`,
        image: sprite,
        animation: 'motion',
        animations: animations,
        frameRate: frameRate,
      });

      that.ui.layers.main.add(imageSprite);
      that.ui.layers.main.batchDraw();
      imageSprite.start();
    };
  }

  draw_custom(
    obj_name: string,
    x: number,
    y: number,
    val: any = null,
    isGoal: boolean = false
  ) {
    let imagePath = this.tileMap[obj_name];
    let [cx, cy] = this.point2cxy(x, y);

    let radius = (0.4 * this.bs) / 2;
    let group = new Konva.Group({
      x: cx + LEFT_PADDING + (this.bs - radius) - MARGIN_NUMBER_CIRCLE,
      y: cy - this.bs / 2 + (this.bs - radius) - MARGIN_NUMBER_CIRCLE,
    });

    if (!isGoal && !!val) {
      let circle = new Konva.Circle({
        radius: radius,
        fill: 'white',
        stroke: '#aaa',
        opacity: 0.9,
      });

      let TEXT_MARGIN =
        val > 9 ? MARGIN_NUMBER_CIRCLE : 2 * MARGIN_NUMBER_CIRCLE;
      let fontSize = Math.ceil((this.bs * 14) / 50); // when bs = 50 fontSize=14
      let num = new Konva.Text({
        text: `${val}`,
        fontSize: fontSize,
        name: `obj-${x}-${y}-text`,
        offsetX: circle.x() + radius - TEXT_MARGIN,
        offsetY: circle.y() + radius - TEXT_MARGIN,
      });
      group.add(circle, num);
    }

    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + LEFT_PADDING,
        y: cy - this.bs / 2,
        width: this.bs,
        height: this.bs,
        name: `obj-${x}-${y}-img`,
      });

      if (isGoal) {
        node.cache();
        node.filters([Konva.Filters.Grayscale]);
        this.ui.layers.main.add(node);
      } else {
        this.ui.layers.main.add(node);
        this.ui.layers.main.add(group);
      }
      this.ui.layers.main.batchDraw();
    });
  }

  draw_drop_goals(goals = []) {
    goals.map((goal) => {
      //@ts-ignore
      this.draw_custom(goal.obj_name, goal.x, goal.y, goal.val, true);
    });
  }

  update_stats(stats = {}) {
    this.stats = stats;
    this.draw_updated_stats();
  }

  parse_value(val: number | string) {
    if (!val) return 0;
    if (_isNumber(val)) return val;
    else {
      const [min_val, max_val] = val.split('-').map((zz) => parseInt(zz));
      return _random(min_val, max_val);
    }
  }

  draw_border() {
    let box = new Konva.Rect({
      x: 50,
      y: this.bs / 2,
      stroke: 'darkred',
      strokeWidth: 10,
      closed: true,
      width: this.width,
      height: this.height,
    });

    this.ui.layers.main.add(box);
  }

  draw_grid() {
    this.draw_cols();
    this.draw_rows();
    this.draw_walls();
    this.draw_tiles();
  }

  _draw_tile(x: number, y: number, tile: string) {
    let [cx, cy] = this.point2cxy(x, y);
    let imagePath = this.tileMap[tile];
    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + 50,
        y: cy - this.bs / 2,
        width: this.bs,
        height: this.bs,
        name: `obj-${x}-${y}-tilebg`,
      });
      this.ui.layers.bg.add(node);
      this.ui.layers.bg.batchDraw();
    });
  }

  draw_tiles() {
    this.tiles.forEach((list: any, row: number) => {
      list.forEach((tile: any, col: number) => {
        if (!!tile) {
          this._draw_tile(row + 1, col + 1, tile);
        }
      });
    });
  }

  draw_cols() {
    for (let col = 1; col < this.cols; col++) {
      let line = new Konva.Line({
        x: 50,
        y: this.bs / 2,
        stroke: 'gray',
        points: [col * this.bs, 5, col * this.bs, this.height - 5],
      });

      let count = new Konva.Text({
        text: `${col}`,
        y: this.height + 40,
        x: col * this.bs + 25,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `${this.cols}`,
      y: this.height + 40,
      x: this.cols * this.bs + 25,
    });

    this.ui.layers.main.add(last_count);
  }

  draw_rows() {
    for (let row = 1; row < this.rows; row++) {
      let line = new Konva.Line({
        x: 50,
        y: this.bs / 2,
        stroke: 'gray',
        points: [this.width - 5, row * this.bs, 5, row * this.bs],
      });

      let count = new Konva.Text({
        text: `${this.rows + 1 - row}`,
        x: this.bs / 2,
        y: row * this.bs - 10,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `1`,
      x: 25,
      y: this.rows * this.bs - 10,
    });

    this.ui.layers.main.add(last_count);
  }

  point2cxy(x: number, y: number) {
    return [(x - 1) * this.bs, this.height - (y - 1) * this.bs];
  }

  draw_wall(x: number, y: number, dir: string, wall_type: string = 'normal') {
    let config = walls_config[wall_type];
    let border = null;
    let [cx, cy] = this.point2cxy(x, y);
    if (dir === 'east') {
      border = new Konva.Line({
        ...config,
        name: `vwall-${x}-${y}`,
        points: [cx + this.bs, cy - this.bs, cx + this.bs, cy],
      });
    }

    if (dir === 'north') {
      border = new Konva.Line({
        name: `hwall-${x}-${y}`,
        ...config,
        points: [cx, cy - this.bs, cx + this.bs, cy - this.bs],
      });
    }

    if (border) this.ui.layers.main.add(border);
  }

  read_message(msg: string, waitFor = 3, img = 'envelope-sprite') {
    let msgBox = new Konva.Text({
      padding: 20,
      align: 'center',
      text: msg,
      fontSize: 18,
    });

    let bubble = new Konva.Rect({
      stroke: '#555',
      strokeWidth: 5,
      fill: '#ddd',
      width: 300,
      height: msgBox.height(),
      shadowColor: 'black',
      shadowBlur: 10,
      shadowOffsetX: 10,
      shadowOffsetY: 10,
      shadowOpacity: 0.2,
      cornerRadius: 10,
    });

    let bubbleImg = new Image();
    bubbleImg.src = this.tileMap['speech_bubble'];
    bubbleImg.onload = function () {
      bubble.fillPatternImage(bubbleImg);
    };

    let group = new Konva.Group({
      x: 120,
      y: 510,
    });

    let tri = new Konva.RegularPolygon({
      sides: 3,
      stroke: '#555',
      strokeWidth: 5,
      radius: 15,
      fill: '#555',
      shadowColor: 'black',
      shadowBlur: 10,
      shadowOffsetX: 10,
      shadowOffsetY: 10,
      shadowOpacity: 0.2,
      x: bubble.x() - 5,
      y: bubble.y() + bubble.height() / 2,
      rotation: 270,
    });

    group.add(tri, bubble, msgBox);

    let that = this;
    this.ui.layers.bg.add(group);

    let tween = new Konva.Tween({
      node: group,
      duration: 1,
      opacity: 0,
      onFinish: () => {
        tween.destroy();
        group.destroy();
        that.ui.stage?.height(that.ui.stageHeight);
      },
    });

    setTimeout(function () {
      tween.play();
    }, waitFor * 1000);

    this.ui.stage?.height(this.ui.stageHeight + bubble.height() + 20);
    this.ui.layers.bg.draw();
  }

  remove_wall(x: number, y: number, dir: string) {
    if (dir !== 'north' && dir !== 'east') return;
    let wall = this.ui.layers.main.find(
      `.${dir === 'north' ? 'hwall' : 'vwall'}-${x}-${y}`
    )[0];
    if (wall) {
      wall.destroy();
    }
    this.ui.layers.main.draw();
  }

  draw_typed_wall(x: number, y: number, dir: string, val: number) {
    let [isGoal, isRemovable, isWall] = _padStart(
      Number(val).toString(2),
      3,
      '0'
    );

    if (parseInt(isWall)) {
      if (parseInt(isRemovable)) {
        this.draw_wall(x, y, dir, 'removable');
      } else {
        this.draw_wall(x, y, dir, 'normal');
      }
    } else if (parseInt(isGoal)) {
      this.draw_wall(x, y, dir, 'goal');
    }
  }

  draw_walls() {
    this.hwalls.forEach((hw: any, i: number) => {
      hw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'north', val);
        } else {
          this.remove_wall(i, j, 'north');
        }
      });
    });

    this.vwalls.forEach((vw: any, i: number) => {
      vw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'east', val);
        } else {
          this.remove_wall(i, j, 'east');
        }
      });
    });
  }
}
