fn main() {
    let s1 = "fn main() {
    let s1 = QSQ;    
    let s2 = s1.replace(81 as char, &(34 as char).to_string());
    let s3 = s2.replace(83 as char, s1);
    println!(Q{}Q, s3);
}";
    let s2 = s1.replace(81 as char, &(34 as char).to_string());
    let s3 = s2.replace(83 as char, s1);
    println!("{}", s3);
}
