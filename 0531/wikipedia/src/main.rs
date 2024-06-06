use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

struct WikiPedia {
    titles: HashMap<usize, String>,
    links: HashMap<usize, Vec<usize>>,
    title_to_id: HashMap<String, usize>,
}

impl WikiPedia {
    fn new(pages_file: &str, links_file: &str) -> WikiPedia {
        let mut titles = HashMap::new();
        let mut links = HashMap::new();
        let mut title_to_id = HashMap::new();

        // check if file exists
        if !Path::new(pages_file).exists() {
            println!("File {} does not exist", pages_file);
            return WikiPedia { titles, links, title_to_id };
        }

        // read pages file into titles
        if let Ok(lines) = read_lines(pages_file) {
            for line in lines {
                if let Ok(ip) = line {
                    let parts: Vec<&str> = ip.trim().split_whitespace().collect();
                    if parts.len() == 2 {
                        let id = parts[0].parse::<usize>().unwrap();
                        let title = parts[1].to_string();
                        titles.insert(id, title.clone());
                        title_to_id.insert(title, id);
                    }
                }
            }
        }
        println!("Finished reading {}", pages_file);
        println!("Read {} titles", titles.len());

        // check if file exists
        if !Path::new(links_file).exists() {
            println!("File {} does not exist", links_file);
            return WikiPedia { titles, links, title_to_id };
        }

        // read links file into links
        if let Ok(lines) = read_lines(links_file) {
            for line in lines {
                if let Ok(ip) = line {
                    let parts: Vec<&str> = ip.trim().split_whitespace().collect();
                    if parts.len() >= 2 {
                        let from = parts[0].parse::<usize>().unwrap();
                        let to = parts[1].parse::<usize>().unwrap();
                        let from_links = links.entry(from).or_insert(Vec::new());
                        // only add links to pages that are in the pages file also check src title exists
                        if titles.contains_key(&to) && titles.contains_key(&from) {
                            from_links.push(to);
                        }                    
                    }
                }
            }
        }
        println!("Finished reading {}", links_file);
        println!("Read {} links", links.len());
        println!("\n");

        WikiPedia { titles, links, title_to_id }
    }

    fn find_shortest_path(&self, src: &str, dst: &str) {
        let src_id = match self.title_to_id.get(src) {
            Some(id) => *id,
            None => {
                println!("Title {} not found", src);
                return;
            }
        };
        let dst_id = match self.title_to_id.get(dst) {
            Some(id) => *id,
            None => {
                println!("Title {} not found", dst);
                return;
            }
        };

        let mut visited = HashSet::new();
        let mut queue = VecDeque::new();
        queue.push_back((src_id, vec![src]));

        while !queue.is_empty() {
            let (node, path) = queue.pop_front().unwrap();
            if node == dst_id {
                println!("Path found: {:?}", path);
                return;
            }
            if let Some(links) = self.links.get(&node) {
                for &link in links {
                    if !visited.contains(&link) {
                        visited.insert(link);
                        let mut new_path = path.clone();
                        new_path.push(self.titles.get(&link).unwrap());
                        queue.push_back((link, new_path));
                    }
                }
            }
        }
        println!("No path found");
    }

    fn find_most_popular_pages(self) {
        // initilize page rank for each page
        let mut page_rank = HashMap::new();
        for (id, _) in &self.titles {
            page_rank.insert(*id, 1.0);
        }

        let num_iterations = 50;
        let damping_factor = 0.85;
        let num_pages = self.titles.len() as f64;

        // calculate page rank
        for _ in 0..num_iterations {
            // for debugging print the sum of the page rank
            let sum: f64 = page_rank.values().sum();
            println!("Sum of page rank: {}", sum);

            let mut new_page_rank = HashMap::new();

            // initialize new pagerank with random surfer probability
            let distribute_rank = 1.0 - damping_factor;
            for (id, _) in &self.titles {
                new_page_rank.insert(*id, distribute_rank); 
            }

            // distribute the current pagerank to the outlinks
            for (&from, links) in &self.links {
                let rank_contribution = damping_factor * page_rank[&from] / links.len() as f64;
                for &to in links {
                    let new_rank = new_page_rank.get_mut(&to).unwrap();
                    *new_rank += rank_contribution;
                }
            } 

            // handle pages with no outlinks
            let sink_rank: f64 = self.titles.keys()
                .filter(|id| self.links.get(id).unwrap_or(&Vec::new()).is_empty())
                .map(|id| page_rank.get(id).unwrap())
                .sum();
            let sink_rank_contribution = damping_factor * sink_rank / num_pages;
            for (_, rank) in &mut new_page_rank {
                *rank += sink_rank_contribution;
            }

            // checks the convergence
            let mut diff = 0.0;
            for (&id, rank) in &new_page_rank {
                diff += (rank - page_rank[&id]).abs();
            }
            println!("Diff: {}", diff);
            if diff < 1e-6 {
                break;
            }

            // update the page rank
            page_rank = new_page_rank;
        }

        // Sort by PageRank
        let mut sorted_page_rank: Vec<_> = page_rank.iter().collect();
        sorted_page_rank.sort_by(|a, b| b.1.partial_cmp(a.1).unwrap());

        //print the most popular pages
        println!("The most popular pages are:");
        for (id, rank) in sorted_page_rank.iter().take(10) {
            if let Some(title) = self.titles.get(id) {
                println!("{}: {}", title, rank)
            }
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(BufReader::new(file).lines())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        println!("Usage: {} <pages_file> <links_file>", args[0]);
        return;
    }
    let pages_file = &args[1];
    let links_file = &args[2];
    let wiki = WikiPedia::new(pages_file, links_file);
    wiki.find_shortest_path("渋谷", "池袋");
    wiki.find_shortest_path("コロラドハイツ大学", "魚沼田中駅");
    // wiki.find_most_popular_pages();
}