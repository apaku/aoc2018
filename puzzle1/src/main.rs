// Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
// License: MIT

use std::io::{BufRead};
use std::collections::HashSet;


fn main() {
    let stdin = std::io::stdin();
    let lines = stdin.lock().lines();
    let changes: Vec<i32> = lines.map(|l|  l.unwrap().parse::<i32>().unwrap()).collect();
    let part1: i32 = changes.iter().sum();
    println!("Part1: {}", part1);
    let mut frequency = 0;
    let mut seenfrequencies = HashSet::new();
    for change in changes.iter().cycle() {
        if seenfrequencies.contains(&frequency) {
            println!("Part2: {}", frequency);
            break;
        }
        seenfrequencies.insert(frequency);
        frequency += change;
    }
}
