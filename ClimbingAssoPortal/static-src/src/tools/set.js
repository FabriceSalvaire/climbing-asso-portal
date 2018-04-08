/***************************************************************************************************
 *
 * Climbing Asso Portal
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

// https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/Set

Set.prototype.isSuperset = function(subset) {
  for (var elem of subset) {
    if (!this.has(elem)) {
      return false;
    }
  }
  return true;
}

Set.prototype.union = function(set_b) {
  var union = new Set(this);
  for (var elem of set_b) {
    union.add(elem);
  }
  return union;
}

Set.prototype.intersection = function(set_b) {
  var intersection = new Set();
  for (var elem of set_b) {
    if (this.has(elem)) {
      intersection.add(elem);
    }
  }
  return intersection;
}

Set.prototype.difference = function(set_b) {
  var difference = new Set(this);
  for (var elem of set_b) {
    difference.delete(elem);
  }
  return difference;
}

/**************************************************************************************************/

// let union = new Set([...a, ...b]);
// let intersection = new Set([...a].filter(x => b.has(x)));
// let difference = new Set([...a].filter(x => !b.has(x)));
