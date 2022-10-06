
use magic_crypt::{new_magic_crypt, MagicCryptTrait};
extern crate openssl;
use urlencoding::decode;

use openssl::rsa::{Rsa, Padding};

use std::{path::Path, fs, process};

use serenity::{
    async_trait,
    futures::StreamExt,
    model::{gateway::Ready, id::ChannelId},
    prelude::*,
};

const GREETING: &str = "[-] Deploying Rustomware";

fn encrypt_small_file(
    filepath: &str,
    dist: &str,
    key: &str,
) -> Result<(), anyhow::Error> {
    let file_data = fs::read_to_string(filepath)?;
    let rsa = Rsa::public_key_from_pem(key.trim().as_bytes()).unwrap();
    let mut buf: Vec<u8> = vec![0; rsa.size() as usize];
    let _ = rsa.public_encrypt(&file_data.as_bytes(), &mut buf, Padding::PKCS1).unwrap();
    fs::write(&dist, buf)?;
    
    Ok(())
}

fn encrypting_files(secrets: Vec<String>) -> Result<(), anyhow::Error> {
    let public_key = &secrets[0];

    let public_key_pem = decrypt_keys(public_key);
    println!("  [-] Encrypting flag.txt to flag.txt.encrypted");
    let b = Path::new("flag.txt").exists();
    if b == true {
        encrypt_small_file(
            "flag.txt",
            "flag.txt.encrypted",
            &public_key_pem,
        )?;
        println!("      [+] Done");
        Ok(())
    } else {
        println!("!!!!! 'flag.txt' file was not found, please create one !!!!!");
        process::exit(0x1337);
    }
}

fn decrypt_keys(enc: &str) -> String {
    let mc = new_magic_crypt!(GREETING, 256);
    let decrypted = mc.decrypt_base64_to_string(&enc).unwrap();
    let res =decode(&decrypted).expect("UTF-8");
    res.to_string()
}

fn get_token() -> String {
    let enc = "Ip/Mf1a/Rgi0iLjZWBKAe6qJcUPNOoRTJ2mKzd1N9hpLpw69ymBlGy3JZwwxJI61+wYBecRLiXFtdERD6X3cNj1PWVoM6iKCqssSVYj4g6Q=";
    let mc = new_magic_crypt!(GREETING, 256);
    let res = mc.decrypt_base64_to_string(&enc).unwrap();
    res
}

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: Context, _ready: Ready) {
        println!("  [+] Done");
        let mut secrets = Vec::new();
        let secret_channel_id = ChannelId(1006632078659555408);
        println!("[-] Getting the secret key");
        let mut messages = secret_channel_id.messages_iter(&ctx).boxed();
        while let Some(message_result) = messages.next().await {
            match message_result {
                Ok(message) => secrets.push(message.content),
                Err(error) => eprintln!("Uh oh! Error: {}", error),
            }
        }
        println!("  [+] Done");
        println!("[-] Encrypting Files");
        let _enc = encrypting_files(secrets);
        println!("  [+] Done");
        println!("[+] Have a nice day!");
        process::exit(0x1337);
    }
}

#[tokio::main]
async fn main() {
    println!("{}", GREETING);
    let x = get_token();
    let mut client = Client::builder(&x)
        .event_handler(Handler)
        .await
        .expect("Err creating client");
    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}