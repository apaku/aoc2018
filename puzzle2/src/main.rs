// Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
// License: MIT

use std::io::{BufRead};
use std::collections::HashMap;

fn part1(lines: &Vec<String>) -> i32 {
    let mut numdoubles = 0;
    let mut numtripples = 0;
    for line in lines {
        let mut char_counts = HashMap::new();
        for ch in line.chars() {
            let newvalue = char_counts.get(&ch).unwrap_or(&0) + 1;
            char_counts.insert(ch, newvalue);
        }
        let mut double_found = false;
        let mut triple_found = false;
        for (_, count) in char_counts.iter() {
            if double_found && triple_found {
                break;
            }
            if *count == 2 && !double_found {
                double_found = true;
                numdoubles += 1;
            }
            if *count == 3 && !triple_found {
                triple_found = true;
                numtripples += 1;
            }
        }
    }
    return numdoubles * numtripples;
}

fn findmismatch(l: &str, r: &str) -> Option<usize> {
    let lchars = l.chars();
    for (i, item) in lchars.enumerate() {
        let tmp = r.chars().nth(i);
        let rchar: char = tmp.unwrap();
        if item != rchar {
            return Some(i);
        }
    }
    return None;
}

fn boxids(head: &String, tail: &Vec<String>) -> Option<String> {
    for line in tail {
        let nonmatchidx = findmismatch(head, line);
        if nonmatchidx.is_none() {
            continue;
        }
        let idx = nonmatchidx.unwrap() + 1;
        let morenonmatch = findmismatch(head.get(idx..).unwrap(),line.get(idx..).unwrap());
        if morenonmatch.is_none() {
            let mut merge = head.get(..nonmatchidx.unwrap() ).unwrap().to_owned();
            merge.push_str(head.get(idx..).unwrap());
            return Some(merge);
        }
    }
    if tail.len() > 1 {
        let (subhead, subtail) = tail.split_first().unwrap();
        let boxid = boxids(subhead, &subtail.to_vec());
        if boxid.is_some() {
            return boxid;
        }
    }
    return None;
}

fn part2(lines: &Vec<String>) -> Option<String> {
    let (head, tail) = lines.split_first().unwrap();
    return boxids(head, &tail.to_vec());
}

fn main() {
    let stdin = std::io::stdin();
    let lines: Vec<String> = stdin.lock().lines().map(|l| l.unwrap()).collect();
    println!("Part1: {}", part1(&lines));
    println!("Part2: {:?}", part2(&lines));
}
