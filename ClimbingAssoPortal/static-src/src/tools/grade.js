/***************************************************************************************************
 *
 * Climbing Grade
 * Copyright (C) 2018 Fabrice Salvaire
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

/*
 * for (let grade of grade_iter(2, 5))
 *     console.log(grade);
 *
 * var grade = new FrenchGrade('5c+');
 * console.log(grade.number);
 * console.log(grade.letter);
 * console.log(grade.sign);
 * console.log(grade.str);
 * console.log(grade.float);
 */

const GRADE_PLUS = 5;

export
class FrenchGrade {
    static * grade_iter(grade_min=1, grade_max=9, grade_plus=GRADE_PLUS) {
	for (var major = grade_min; major <= grade_max; major++)
	    for (var minor of ['a', 'b', 'c']) {
		var grade = major.toString() + minor;
		yield grade; // Fixme: FrenchGrade ???
		if (major >= GRADE_PLUS)
                    yield grade + '+';
	    }
    }

    constructor(grade) {
	var grade = grade.toLowerCase();
	var grade_re = /([1-9])([a-c])?(\+|\-)?/;
	var match = grade_re.exec(grade);
	if (match === null)
	    console.log('Invalid grade', grade);
	var [number, letter, sign] = match.slice(1,4);
	if (number) {
	    this._number = parseInt(number);
	    if (letter) {
		if (sign === '-')
		    throw `Bad grade "${grade}" mixing letter and inf`;
		else if (sign === '+' && number < GRADE_PLUS)
		    throw `Bad grade "${grade}" with sup < ${GRADE_PLUS}`;
	    }
	    this._letter = letter;
	    this._sign = sign;
	}
    }

    get number() {
	return this._number;
    }

    get letter() {
	return this._letter;
    }

    get sign() {
	return this._sign;
    }

    get str() {
	var grade = this._number.toString();
	if (this._letter)
            grade += this._letter;
        if (this._sign)
            grade += this._sign;
        return grade;
    }

    get float() {
        var value = this._number;
        var letter = this._letter;
        var sign = this._sign;

        if (letter) {
            // 6a < 6a+ < 6b < 6b+ < 6c < 6c+ < 7a
            if (letter === 'a')
                value += 1/4;
            else if (letter === 'b')
                value += 1/2
            else // c
                value += 3/4
            if (sign === '+')
                value += 1/8
	} else {
	    // Old system: 5 -/inf < 5 < 5 +/sup
            if (sign === '-')
                value += 1/4;
            else if (sign)
                value += 1/2;
            else
                value += 3/4;
	}

        return value;
    }
}
