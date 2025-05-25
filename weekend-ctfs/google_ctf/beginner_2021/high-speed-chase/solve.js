const a = scanArray
const left = a.slice(0,8)
const mid = a.slice(7,9)
const right = a.slice(9,16)

let lefta = 0
count = 2.25
for (let i = 0; i < left.length; i++) {
 if (left[i] != 0) {
  count ++
  lefta += left[i]
 }
}
lefta -= Math.max(...left)
lefta /= count


let righta = 0
count = 2.25
for (let i = 0; i < right.length; i++) {
 if (right[i] != 0) {
  count ++
  righta += right[i]
 }
}
righta -= Math.max(...right)
righta /= count

let mida = 0
count = 5 // need this 
for (let i = 0; i < mid.length; i++) {
 if (mid[i] != 0) {
  count ++ 
  mida += mid[i] 
 }
}
mida -= Math.max(...mid)
mida /= count


if (Math.max(lefta, mida, righta) == lefta) {
	return -1
} else if (Math.max(lefta, mida, righta) == righta) {
	return 1
} else {
	return 0
}
// flag: CTF{cbe138a2cd7bd97ab726ebd67e3b7126707f3e7f}
