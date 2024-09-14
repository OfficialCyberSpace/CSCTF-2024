#[macro_use]
extern crate litcrypt;
use_litcrypt!();
use std::io;
use std::process;
use std::io::Write;
use rand_pcg::Pcg64;
use rand_seeder::Seeder;
use rand::prelude::*;
use salsa20::Salsa20;
use salsa20::cipher::{KeyIvInit, StreamCipher};
use base64::prelude::*;
extern crate rot13;
use aes::Aes128;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use rc4::{Rc4};
use rc4::KeyInit;

fn get_key() -> [u8; 32] {
    let key = lc!("y0u_w0nt_gu3ss_th1s");
    let mut rng: Pcg64 = Seeder::from(key).make_rng();
    let seed = rng.gen::<[u8; 32]>(); 
    return seed;
}
 
fn get_nonce() -> [u8; 8] {
    let key = lc!("y3t_4n0th3r_p4ssw0rd");
    let mut rng: Pcg64 = Seeder::from(key).make_rng();
    let seed = rng.gen::<[u8; 8]>();
    return seed;
}

fn encrypt(){
    let key = get_key();
    let nonce = get_nonce();
    let mut cipher = Salsa20::new(&key.into(), &nonce.into());
    println!("What do you want to encrypt?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    let mut buffer = plaintext.into_bytes();
    cipher.apply_keystream(&mut buffer);
    let ciphertext = buffer.clone();
    println!("Here your encrypted text:");
    println!("{}", hex::encode(ciphertext));
}

fn base64decode() {
    println!("What do you want to decode?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    plaintext = plaintext.trim().to_string();

    let decoded_bytes = match BASE64_STANDARD.decode(&plaintext) {
        Ok(decoded) => decoded,
        Err(_) => {
            println!("Invalid Base64 input.");
            return;
        }
    };

    let decoded_string = match String::from_utf8(decoded_bytes) {
        Ok(string) => string,
        Err(_) => {
            println!("Something went wrong! Try again.");
            return;
        }
    };

    println!("Here your decoded data: {:?}", decoded_string);
}

fn base64encode() {
    println!("What do you want to encode?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    plaintext = plaintext.trim().to_string();
    let output = BASE64_STANDARD.encode(plaintext);
    println!("Here your encoded data: {:?}", output);
}

fn base64() {
    println!("Choose your what you want to do:\n[1] Encode\n[2] Decode");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut option = String::new();
    io::stdin()
        .read_line(&mut option)
        .expect("Failed to read input.");
    let option: u32 = match option.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Invalid option!");
            return;
        }
    };

    match option {
        1 => base64encode(),
        2 => base64decode(),
        _ => {
            println!("Invalid option!");
            return;
        }
    }
}

fn rot13() {
    println!("What do you want to rot13?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    plaintext = plaintext.trim().to_string();
    let output = rot13::rot13(&plaintext);
    println!("Result: {:?}", output);
}

type Aes128Cbc = Cbc<Aes128, Pkcs7>;

fn aesencrypt() {
    let iv = hex::decode(String::from(lc!("1280222000020000100200A020B03030"))).unwrap();
    let key = hex::decode(String::from(lc!("000102030405060708090A0B0C0D0E0F"))).unwrap();
    let cipher = Aes128Cbc::new_from_slices(&key, &iv).unwrap();

    println!("What do you want to encrypt?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    let buffer = plaintext.trim().as_bytes();

    let pos = buffer.len();
    let mut buff = [0u8; 32];
    buff[..pos].copy_from_slice(buffer);

    let ciphertext = cipher.encrypt(&mut buff, pos).unwrap();

    println!("Result: {:?}", hex::encode(ciphertext));
}

fn aesdecrypt() {
    let iv = hex::decode(String::from("1280222000020000100200A020B03030")).unwrap();
    let key = hex::decode(String::from("000102030405060708090A0B0C0D0E0F")).unwrap();
    let cipher = Aes128Cbc::new_from_slices(&key, &iv).unwrap();

    println!("What do you want to decrypt?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    
    let buff = hex::decode(&plaintext.trim());
    let mut buff = match buff {
        Ok(bytes) => bytes,
        Err(e) => {
            eprintln!("Error decoding hex: {}", e);
            return;
        }
    };
    let decrypted_ciphertext = match cipher.decrypt(&mut buff) {
        Ok(string) => string,
        Err(_) => {
            println!("Somethin went wrong!");
            return;
        }
    };
    println!("Result: {:?}", std::str::from_utf8(decrypted_ciphertext).unwrap());
}

fn aes() {
    println!("Choose your what you want to do:\n[1] Encrypt\n[2] Decrypt");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut option = String::new();
    io::stdin()
        .read_line(&mut option)
        .expect("Failed to read input.");
    let option: u32 = match option.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Invalid option!");
            return;
        }
    };

    match option {
        1 => aesencrypt(),
        2 => aesdecrypt(),
        _ => {
            println!("Invalid option!");
            return;
        }
    }
}

fn rc4encrypt() {
    println!("What do you want to encrypt?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");
    let mut buff = plaintext.trim().as_bytes().to_vec();

    let key_str = lc!("This_Is_Muy_Sup3r_Str0ng_KEY_3232");
    let key = key_str.as_bytes();
    let mut key_array = [0u8; 33];
    key_array.copy_from_slice(key);

    let mut rc4 = Rc4::new(&key_array.into());
    rc4.apply_keystream(&mut buff);

    println!("Result: {:?}", hex::encode(buff));
}

fn rc4decrypt() {
    println!("What do you want to decrypt?");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut plaintext = String::new();
    io::stdin()
        .read_line(&mut plaintext)
        .expect("Failed to read input.");

    let buff = hex::decode(&plaintext.trim());
    let mut buff = match buff {
        Ok(bytes) => bytes,
        Err(e) => {
            eprintln!("Error decoding hex: {}", e);
            return;
        }
    };

    let key_str = lc!("This_Is_Muy_Sup3r_Str0ng_KEY_3232");
    let key = key_str.as_bytes();
    let mut key_array = [0u8; 33];
    key_array.copy_from_slice(key);

    let mut rc4 = Rc4::new(&key_array.into());
    rc4.apply_keystream(&mut buff);

    println!("Result: {:?}", std::str::from_utf8(&buff).unwrap());
}

fn rc4() {
    println!("Choose your what you want to do:\n[1] Encrypt\n[2] Decrypt");
    print!("> ");
    io::stdout().flush().unwrap();
    let mut option = String::new();
    io::stdin()
        .read_line(&mut option)
        .expect("Failed to read input.");
    let option: u32 = match option.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Invalid option!");
            return;
        }
    };

    match option {
        1 => rc4encrypt(),
        2 => rc4decrypt(),
        _ => {
            println!("Invalid option!");
            return;
        }
    }
}

fn main(){
    println!(r"
 _______ .__   __.   _______  __  .__   __.  _______ 
|   ____||  \ |  |  /  _____||  | |  \ |  | |   ____|
|  |__   |   \|  | |  |  __  |  | |   \|  | |  |__   
|   __|  |  . `  | |  | |_ | |  | |  . `  | |   __|  
|  |____ |  |\   | |  |__| | |  | |  |\   | |  |____ 
|_______||__| \__|  \______| |__| |__| \__| |_______|
");
    println!("Welcome to my engine!\n");

    loop {
        println!("Choose the option you want to use in my engine:");
        println!("[1] Base64\n[2] Rot13\n[3] AES\n[4] RC4\n[5] exit");
        print!("> ");
        io::stdout().flush().unwrap();

        let mut option = String::new();
        io::stdin().read_line(&mut option).expect("Failed to read input.");

        let option: u32 = match option.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("Invalid option!");
                return;
            }
        };

        match option {
            1 => base64(),
            2 => rot13(),
            3 => aes(),
            4 => rc4(),
            5 => {
                println!("Exiting program.");
                return;
            },
            1337 => encrypt(),
            _ => {
                println!("Invalid option!");
                process::exit(1);
            }
        }
    }
}