package main

import "C"

import (
	"fmt"
	//"reflect"
	"os"
	"github.com/brentp/vcfgo"
	"github.com/brentp/xopen"
	"github.com/mwatkin8/copy_go-vmc/vmc"
	"log"
)

//export Transform
func Transform() {

	fh, err := xopen.Ropen("../static/uploads/test.vcf")
	eCheck(err)
	defer fh.Close()

	rdr, err := vcfgo.NewReader(fh, false)

	// Add VMC INFO to the header.
	rdr.AddInfoToHeader("VMCGSID", "1", "String", "VMC Sequence identifier")
	rdr.AddInfoToHeader("VMCGLID", "1", "String", "VMC Location identifier")
	rdr.AddInfoToHeader("VMCGAID", "1", "String", "VMC Allele identifier")

	eCheck(err)
	defer rdr.Close()

	out := ""
	for {
		variant := rdr.Read()
		if variant == nil {
			break
		}

		// Check for alternate alleles.
		altAllele := variant.Alt()
		if len(altAllele) > 1 {
			log.Panicln("multiallelic variants found, please pre-run vt decomposes.")
		}

		// set variant line to build vmc
		record := vmc.VMCRecord(variant)

		//fmt.Println(record.Location)
		//fmt.Println(variant.String())

		out += variant.String() + ";VMCGSID=" + record.Location.Id + ";VMCGLID=" + record.Location.Interval + ";VMCGAID=" + record.Location.Sequence_id + "\n"
	}

	file, err := os.Create("go.vcf")
    if err != nil {
        log.Fatal("Cannot create file", err)
    }
    defer file.Close()
		fmt.Fprintf(file, out)

	//fmt.Println(reflect.TypeOf(out))
	//return out
}

func main() {}

//export eCheck
func eCheck(p error) {
	if p != nil {
		panic(p)
	}
}
