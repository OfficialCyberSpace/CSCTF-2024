extern crate rand;
extern crate termion;
use rand::Rng;
use std::io::{stdout, Read, Write};
use std::thread::sleep;
use std::time::Duration;
use std::vec::Vec;
use termion::raw::IntoRawMode;
use termion::{async_stdin, clear, color, cursor, style};
use magic_crypt::MagicCryptTrait;
#[macro_use] extern crate magic_crypt;
#[macro_use] extern crate litcrypt;
use_litcrypt!();


const BORDER: char = '■';
#[derive(PartialEq, Copy, Clone)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(PartialEq, Copy, Clone)]
pub struct BodyPart {
    x: u16,
    y: u16,
    part: char,
    direction: Direction,
}

pub struct Snake {
    body: Vec<BodyPart>,
}

pub struct Game<T, F> {
    stdout: T,
    stdin: F,
    snake: Snake,
    food: (u16, u16),
    score: i32,
    highscore: i32,
    last_dir: u8,
    speed: u64,
    width: u16,
    height: u16,
}

impl<T: Write, F: Read> Game<T, F> {
    ///creates and resets field
    fn print_field(&mut self) {
        write!(
            self.stdout,
            "{}{}{}",
            clear::All,
            cursor::Goto(1, 1),
            color::Fg(color::Blue)
        )
        .unwrap();
        self.stdout.flush().unwrap();
        for i in 0..self.height {
            write!(self.stdout, "{}", cursor::Goto(1, i + 1 as u16)).unwrap();
            write!(self.stdout, "{}", BORDER).unwrap();
            write!(self.stdout, "{}", cursor::Goto(self.width, i + 1 as u16)).unwrap();
            write!(self.stdout, "{}", BORDER).unwrap();
        }
        for i in 0..self.width {
            write!(self.stdout, "{}", cursor::Goto(i + 1 as u16, 1)).unwrap();
            write!(self.stdout, "{}", BORDER).unwrap();
            write!(self.stdout, "{}", cursor::Goto(i + 1 as u16, self.height)).unwrap();
            write!(self.stdout, "{}", BORDER).unwrap();
        }
        write!(self.stdout, "{}", color::Fg(color::Reset)).unwrap();
        self.stdout.flush().unwrap();
    }

    #[inline(always)]
    fn win(&mut self) -> bool {
        if (self.score ^ 0x9872) == 0xd8ff {
            return true
        }
        false
    }

    ///w,a,s,d or h,j,k,l to move snake and redraw everything
    fn move_snake(&mut self) -> bool {
        let mut key = [0];
        self.stdin.read(&mut key).unwrap();
        if key[0] == self.last_dir {
            let mut key: [u8; 100] = [0; 100];
            self.stdin.read(&mut key).unwrap();
            self.automove();
        } else {
            match key[0] {
                b'q' | b'Q' => return false,
                b'w' | b'k'
                    if self.snake.body[0].direction != Direction::Down
                        && self.snake.body[0].direction != Direction::Up =>
                {
                    self.take_direction(Direction::Up)
                }
                b'a' | b'h'
                    if self.snake.body[0].direction != Direction::Right
                        && self.snake.body[0].direction != Direction::Left =>
                {
                    self.take_direction(Direction::Left)
                }
                b'd' | b'l'
                    if self.snake.body[0].direction != Direction::Left
                        && self.snake.body[0].direction != Direction::Right =>
                {
                    self.take_direction(Direction::Right)
                }
                b's' | b'j'
                    if self.snake.body[0].direction != Direction::Up
                        && self.snake.body[0].direction != Direction::Down =>
                {
                    self.take_direction(Direction::Down)
                }
                b' ' => {
                    let mut key = [0];
                    loop {
                        self.stdin.read(&mut key).unwrap();
                        if let b' ' = key[0] {
                            break;
                        }
                    }
                }
                _ => self.automove(),
            }
        }
        self.last_dir = key[0];
        self.check_food();
        self.print_snake();
        return true;
    }

    ///keeps the snake moving
    fn automove(&mut self) {
        self.take_direction(self.snake.body[0].direction);
    }

    ///change direction of the snake to all parts and make it move
    fn take_direction(&mut self, dir: Direction) {
        write!(
            self.stdout,
            "{} ",
            cursor::Goto(
                self.snake.body[self.snake.body.len() - 1].x,
                self.snake.body[self.snake.body.len() - 1].y
            )
        )
        .unwrap();
        for i in (0..self.snake.body.len()).rev() {
            if i != 0 {
                self.snake.body[i].direction = self.snake.body[i - 1].direction;
                self.snake.body[i].x = self.snake.body[i - 1].x;
                self.snake.body[i].y = self.snake.body[i - 1].y;
            }
        }
        self.snake.body.iter_mut().take(1).for_each(|head| {
            match dir {
                Direction::Up => {
                    head.part = '▲';
                    head.y -= 1;
                }
                Direction::Down => {
                    head.part = '▼';
                    head.y += 1;
                }
                Direction::Left => {
                    head.part = '◀';
                    head.x -= 1;
                }
                Direction::Right => {
                    head.part = '▶';
                    head.x += 1;
                }
            }
            head.direction = dir;
        });
    }

    ///when snake eats food it grows by one part
    fn grow_snake(&mut self) {
        let snake_size = self.snake.body.len() - 1;
        let tail = self.snake.body[snake_size];
        match tail.direction {
            Direction::Up => {
                self.snake.body.push(BodyPart {
                    x: tail.x,
                    y: tail.y + 1,
                    part: '▪',
                    direction: tail.direction,
                });
            }
            Direction::Down => {
                self.snake.body.push(BodyPart {
                    x: tail.x,
                    y: tail.y - 1,
                    part: '▪',
                    direction: tail.direction,
                });
            }
            Direction::Right => {
                self.snake.body.push(BodyPart {
                    x: tail.x - 1,
                    y: tail.y,
                    part: '▪',
                    direction: tail.direction,
                });
            }
            Direction::Left => {
                self.snake.body.push(BodyPart {
                    x: tail.x + 1,
                    y: tail.y,
                    part: '▪',
                    direction: tail.direction,
                });
            }
        }
        self.score += 10;
        if self.score > self.highscore {
            self.highscore = self.score;
        }
        if self.speed > 100 {
            self.speed -= 20;
        }
        self.print_score();
        self.print_food();
    }

    ///prints the score next to field
    fn print_score(&mut self) {

        write!(
            self.stdout,
            "{}{}Reminder: {}",
            cursor::Goto(self.width + 7, 3),
            color::Fg(color::Red),
            color::Fg(color::Reset)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}{}You need to get exactly 16525 points for the flag{}",
            cursor::Goto(self.width + 7, 4),
            color::Fg(color::Red),
            color::Fg(color::Reset)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}{}Hi-Score: {}{}",
            cursor::Goto(self.width + 7, 5),
            color::Fg(color::Green),
            self.highscore,
            color::Fg(color::Reset)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}{}Score: {}{}",
            cursor::Goto(self.width + 7, 6),
            color::Fg(color::Green),
            self.score,
            color::Fg(color::Reset)
        )
        .unwrap();
        write!(self.stdout, "{}q: quit", cursor::Goto(self.width + 7, 8)).unwrap();
        write!(
            self.stdout,
            "{}Space: pause/start",
            cursor::Goto(self.width + 7, 9)
        )
        .unwrap();
        self.stdout.flush().unwrap();
    }

    ///reprint snake
    fn print_snake(&mut self) {
        for i in self.snake.body.iter() {
            write!(
                self.stdout,
                "{}{}{}{}",
                cursor::Goto(i.x, i.y),
                color::Fg(color::Green),
                i.part,
                color::Fg(color::Reset)
            )
            .unwrap();
        }
        self.stdout.flush().unwrap();
    }

    ///check if snake hit a wall or itself
    fn check_game_over(&mut self) -> bool {
        for i in 0..self.width {
            if self.snake.body[0].x == i
                && (self.snake.body[0].y == 1 || self.snake.body[0].y == self.height)
            {
                return true;
            }
        }
        for i in 0..self.height {
            if self.snake.body[0].y == i
                && (self.snake.body[0].x == 1 || self.snake.body[0].x == self.width)
            {
                return true;
            }
        }
        let mut head = true;
        for i in self.snake.body.iter() {
            if head == false {
                if self.snake.body[0].x == i.x && self.snake.body[0].y == i.y {
                    return true;
                }
            }
            head = false;
        }
        false
    }

    ///check if snake found food to eat
    fn check_food(&mut self) {
        if self.snake.body[0].x == self.food.0 && self.snake.body[0].y == self.food.1 {
            self.food = food_gen(self.width, self.height);
            loop {
                if self.validate_food() {
                    break;
                }
            }
            self.grow_snake();
        }
    }

    ///check if food is spawned on the snake and try again
    fn validate_food(&mut self) -> bool {
        for i in self.snake.body.iter() {
            if i.x == self.food.0 && i.y == self.food.1 {
                self.food = food_gen(self.width, self.height);
                return false;
            }
        }
        true
    }

    ///reprint food
    fn print_food(&mut self) {
        let food = "#";
        write!(
            self.stdout,
            "{}{}{}{}",
            cursor::Goto(self.food.0, self.food.1),
            color::Fg(color::Red),
            food,
            color::Fg(color::Reset)
        )
        .unwrap();
        self.stdout.flush().unwrap();
    }

    ///print game over screen
    fn print_game_over(&mut self) {
        let (screen_width, screen_width_border) = {
            if self.width as i32 / 2 - 8 < 0 {
                (1, 17)
            } else {
                (self.width / 2 - 8, self.width / 2 + 8)
            }
        };
        let screen_height = {
            if self.height as i32 / 2 - 3 < 0 {
                1
            } else {
                self.height / 2 - 3
            }
        };
        write!(
            self.stdout,
            "{}-----------------",
            cursor::Goto(screen_width, screen_height)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|   Game Over!  |",
            cursor::Goto(screen_width, screen_height + 1)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|HighScore: {}  {}|",
            cursor::Goto(screen_width, screen_height + 2),
            self.score,
            cursor::Goto(screen_width_border, screen_height + 2)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|Score: {}    {}|",
            cursor::Goto(screen_width, screen_height + 3),
            self.score,
            cursor::Goto(screen_width_border, screen_height + 3)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|(r)etry  (q)uit|",
            cursor::Goto(screen_width, screen_height + 4)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}-----------------",
            cursor::Goto(screen_width, screen_height + 5)
        )
        .unwrap();
        self.stdout.flush().unwrap();
    }
    fn print_game_over_win(&mut self) {
        write!(
            self.stdout,
            "{}{}{}{}",
            clear::All,
            style::Reset,
            cursor::Show,
            cursor::Goto(1, 1)
        )
        .unwrap();
        let (screen_width, _screen_width_border) = {
            if self.width as i32 / 2 - 8 < 0 {
                (1, 17)
            } else {
                (self.width / 2 - 8, self.width / 2 + 8)
            }
        };
        let screen_height = {
            if self.height as i32 / 2 - 3 < 0 {
                1
            } else {
                self.height / 2 - 3
            }
        };
        write!(
            self.stdout,
            "{}----------------------------------------",
            cursor::Goto(screen_width-9, screen_height - 3)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|              Game Over!              |",
            cursor::Goto(screen_width-9, screen_height - 2)
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|Score: {}                             |",
            cursor::Goto(screen_width-9, screen_height - 1),
            self.score
        )
        .unwrap();
        write!(
            self.stdout,
            "{}|Flag: {} |",
            cursor::Goto(screen_width-9, screen_height),
            decrypt("N382twfN/gmXhsFW2n7nJ8bwqlrdLlp3YpDpxpKQOjxcSqtcgQ7vYegov4lNfQQM")
        )
        .unwrap();
        write!(
            self.stdout,
            "{}----------------------------------------",
            cursor::Goto(screen_width-9, screen_height + 1)
        )
        .unwrap();
        self.stdout.flush().unwrap();
    }
    ///game begins, everything is printed and checks snake movement
    fn start_snake_game(&mut self) {
        write!(self.stdout, "{}", cursor::Hide).unwrap();
        self.print_field();
        self.print_score();
        self.print_food();
        self.print_snake();
        loop {
            if !self.move_snake() {
                break;
            }
            if self.check_game_over() {
                break;
            };
            if self.win(){
                break;
            };
            sleep(Duration::from_millis(self.speed));
        }
        if self.win(){
            self.print_game_over_win();
        }
        else if !self.end_game() {
            self.start_snake_game();
        }
    }

    ///print game over screen and quit or retry
    fn end_game(&mut self) -> bool {
        self.print_game_over();
        loop {
            let mut key = [0];
            self.stdin.read(&mut key).unwrap();
            match key[0] {
                b'r' | b'R' => {
                    self.snake.body = vec![
                        BodyPart {
                            x: self.width / 2,
                            y: self.height / 2,
                            part: '◀',
                            direction: Direction::Left,
                        },
                        BodyPart {
                            x: self.width / 2 + 1,
                            y: self.height / 2,
                            part: '▪',
                            direction: Direction::Left,
                        },
                    ];
                    self.score = 0;
                    self.food = food_gen(self.width, self.height);
                    self.speed = 220;
                    return false;
                }
                b'q' | b'Q' => {
                    write!(
                        self.stdout,
                        "{}{}{}{}",
                        clear::All,
                        style::Reset,
                        cursor::Show,
                        cursor::Goto(1, 1)
                    )
                    .unwrap();
                    self.stdout.flush().unwrap();
                    return true;
                }
                _ => {}
            }
        }
    }
}

///initialize everything(snake, game, score)
fn init(width: u16, height: u16) {
    let stdout = stdout().into_raw_mode().unwrap();
    let stdin = async_stdin();
    let _game = Game {
        stdout,
        stdin,
        snake: Snake {
            body: vec![
                BodyPart {
                    x: width / 2,
                    y: height / 2,
                    part: '◀',
                    direction: Direction::Left,
                },
                BodyPart {
                    x: width / 2 + 1,
                    y: height / 2,
                    part: '▪',
                    direction: Direction::Left,
                },
            ],
        },
        food: food_gen(width, height),
        score: 0,
        highscore: 0,
        last_dir: b'a',
        speed: 100,
        width,
        height,
    }
    .start_snake_game();
}

fn decrypt(x: &str) -> String {
    let key = lc!("Q3liZXJzcGFjZSBSb2NrcyE=");
    let mcrypt = new_magic_crypt!(key, 256);
    let decrypted_string = String::from(mcrypt.decrypt_base64_to_string(x).unwrap());
    return decrypted_string
}
///generate food at a random location
fn food_gen(width: u16, height: u16) -> (u16, u16) {
    let rx = rand::thread_rng().gen_range(2, width);
    let ry = rand::thread_rng().gen_range(2, height);
    (rx, ry)
}
fn main() {
    let height = 20;
    let width = 60;
    if height < 4 || width < 4 {
        println!("Height and width need to be bigger than 4(2 of those are for borders).");
        std::process::exit(1);
    }
    init(width, height);
}