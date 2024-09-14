use std::io;
use std::process;

fn main() {
    println!("Enter the flag: ");
    let mut flag = String::new();

    io::stdin()
        .read_line(&mut flag)
        .expect("Failed to get your input, Try again!");

    if flag.trim().len() != 26 {
        println!("Wrong input length!, Try again!");
        process::exit(1);
    } else {
        let mut x = 0;
        let password: Vec<char> = flag.chars().collect();
        let _0:i32 = password[0] as i32;
        let _1:i32 = password[1] as i32;
        let _2:i32 = password[2] as i32;
        let _3:i32 = password[3] as i32;
        let _4:i32 = password[4] as i32;
        let _5:i32 = password[5] as i32;
        let _6:i32 = password[6] as i32;
        let _7:i32 = password[7] as i32;
        let _8:i32 = password[8] as i32;
        let _9:i32 = password[9] as i32;
        let _10:i32 = password[10] as i32;
        let _11:i32 = password[11] as i32;
        let _12:i32 = password[12] as i32;
        let _13:i32 = password[13] as i32;
        let _14:i32 = password[14] as i32;
        let _15:i32 = password[15] as i32;
        let _16:i32 = password[16] as i32;
        let _17:i32 = password[17] as i32;
        let _18:i32 = password[18] as i32;
        let _19:i32 = password[19] as i32;
        let _20:i32 = password[20] as i32;
        let _21:i32 = password[21] as i32;
        let _22:i32 = password[22] as i32;
        let _23:i32 = password[23] as i32;
        let _24:i32 = password[24] as i32;
        let _25:i32 = password[25] as i32;

        if _11 * _19 * _4 != 391020 {
            x = 1;
        }

        if _8 * _13 * _22 != 567720 {
            x = 1;
        }

        if _0 * _22 + _15 != 4872 {
            x = 1;
        }

        if _8 + _0 + _11 != 199 {
            x = 1;
        }

        if _13 - _12 * _22 != -3721 {
            x = 1;
        }

        if _4 * _9 - _1 != 8037 {
            x = 1;
        }

        if _16 * _9 * _11 != 272832 {
            x = 1;
        }

        if _3 * _23 + _15 != 9792 {
            x = 1;
        }

        if _9 - _23 - _4 != -70 {
            x = 1;
        }   

        if _5 - _21 - _8 != -63 {
            x = 1;
        }

        if _3 * _24 + _0 != 5359 {
            x = 1;
        }

        if _1 * _25 + _17 != 10483 {
            x = 1;
        }

        if _19 * _7 * _2 != 893646 {
            x = 1;
        }

        if _11 - _4 + _19 != 93 {
            x = 1;
        }

        if _6 + _7 - _10 != 136 {
            x = 1;
        }

        if _25 + _0 + _10 != 287 {
            x = 1;
        }

        if _5 + _12 - _22 != 104 {
            x = 1;
        }

        if _12 + _7 * _4 != 8243 {
            x = 1;
        }

        if _1 - _22 + _4 != 81 {
            x = 1;
        }

        if _8 - _11 * _19 != -5503 {
            x = 1;
        }

        if _8 - _10 - _7 != -129 {
            x = 1;
        }

        if _22 + _20 + _21 != 224 {
            x = 1;
        }

        if _23 + _24 + _12 != 232 {
            x = 1;
        }

        if _15 - _9 + _4 != 2 {
            x = 1;
        }

        if _15 * _9 + _2 != 5635 {
            x = 1;
        }

        if _14 + _24 + _16 != 210 {
            x = 1;
        }

        if _10 + _1 - _12 != 125 {
            x = 1;
        }

        if _18 - _1 - _5 != -111 {
            x = 1;
        }

        if _12 - _14 - _7 != -163 {
            x = 1;
        }

        if _5 + _1 - _16 != 158 {
            x = 1;
        }

        if x == 0 {
            println!("Correct!");
        } else {
            println!("Wrong flag, Try again!");
        }
    }
}