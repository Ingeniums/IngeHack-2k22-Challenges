use ext_php_rs::prelude::*;
use secstr::SecVec;

struct Secrets {
    secvec1: SecVec<u8>,
    secvec2: SecVec<u8>,
    username: SecVec<u8>,
    password: SecVec<u8>,
}

fn rusty_secrets() -> Secrets {
    Secrets {
        secvec1: SecVec::from([
            120, 56, 40, 40, 120, 40, 40, 56, 24, 40, 40, 40, 40, 40, 40, 40, 24, 40, 56, 40, 24,
            104, 40, 40, 40, 24, 40, 40, 40, 56, 24, 40, 56, 40, 24,
        ]),
        secvec2: SecVec::from(vec![
            49, 86, 79, 77, 48, 73, 75, 83, 99, 90, 27, 94, 27, 90, 91, 27, 71, 92, 80, 27, 71, 63,
            27, 27, 74, 71, 95, 25, 92, 80, 71, 88, 80, 88, 101,
        ]),
        username: SecVec::from(vec![118, 118, 120, 104, 105, 100]),
        password: SecVec::from(vec![
            105, 110, 103, 101, 104, 97, 99, 107, 99, 116, 102, 50, 48, 50, 50,
        ]),
    }
}

fn xor(p: Vec<u8>, k: Vec<u8>) -> Vec<u8> {
    let l = p.iter().zip(k.iter()).map(|(&x1, &x2)| x1 ^ x2).collect();
    l
}

#[php_function(ignore_module)]
pub fn inge_gateway(user: &str, password: &str) -> String {
    let secrets = rusty_secrets();
    let mut v1 = vec![116, 51, 97, 109, 48, 115, 51, 118, 51, 110];
    let mut v2 = vec![114, 117, 115, 116, 121, 99, 116, 102, 49, 51, 51, 55];
    v1.reverse();
    v2.reverse();
    let v3 = xor(secrets.username.unsecure().to_vec(), v1);
    let v4 = xor(secrets.password.unsecure().to_vec(), v2);

    let u = String::from_utf8(v3).expect("");
    let p =  String::from_utf8(v4).expect("");

    if String::from(user) == u
        && String::from(password) == p
    {
        let win = xor(
            secrets.secvec1.unsecure().to_vec(),
            secrets.secvec2.unsecure().to_vec(),
        );
        format!("{:?}", win)
    } else {
        format!("")
    }
}

#[php_module]
pub fn get_module(module: ModuleBuilder) -> ModuleBuilder {
    module
}
